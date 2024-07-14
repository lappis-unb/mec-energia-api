
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist

from . import serializers
from .requests_permissions import RequestsPermissions

from utils.user.user_type_util import UserType
from utils.user.authentication import create_token_response, create_valid_token_response


class Authentication(ObtainAuthToken):
    @swagger_auto_schema(responses={200: serializers.AuthenticationTokenSerializerForDocs()})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                            context={'request': request})

            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']

            if not user.account_password_status in ['OK', 'user_reset']:
                raise Exception('Usuário não pode fazer login no sistema')
            
            try:
                existing_token = Token.objects.get(user=user)
                existing_token.delete()
            except Token.DoesNotExist:
                pass

            token = Token.objects.create(user=user)
        except Exception as error:
            return Response({'Authentication error': f'{str(error)}'}, status.HTTP_401_UNAUTHORIZED)

        try:
            UserType.is_valid_user_type(user.type)
            response = Authentication._create_and_update_login_response(token.key, user.id, user.email, user.first_name, user.last_name, user.type)

            return Response(response)
        except Exception as error:
            return Response({'Authentication error': f'{str(error)}'}, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(query_serializer=serializers.AuthenticationGetTokenParamsSerializer,
                        responses={200: serializers.AuthenticationGetTokenSerializerForDocs()})
    def get(self, request, *args, **kwargs):
        params_serializer = serializers.AuthenticationGetTokenParamsSerializer(data=request.data)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            Token.objects.get(pk=request.data['token'])

            is_valid_token = True
        except ObjectDoesNotExist:
            is_valid_token = False

        response = create_valid_token_response(is_valid_token)

        return Response(response)
    
    def _invalid_sessions_tokens(user):
        sessions_tokens = Token.objects.filter(user=user)

        if sessions_tokens:
            sessions_tokens.delete()

    def _create_and_update_login_response(token, user_id, user_email, user_first_name, user_last_name, user_type):
        response = create_token_response(token, user_id, user_email, user_first_name, user_last_name, user_type)

        if user_type in RequestsPermissions.university_user_permissions:
            user = RequestsPermissions.get_university_user_object(user_id)
            university_id = user.university.id

            response = Authentication._update_university_user_response(response, university_id)

        return response

    def _update_super_user_response(response):
        return response

    def _update_university_user_response(response, university_id):
        response = Authentication._insert_university_id_on_response(response, university_id)
        
        return response

    def _insert_university_id_on_response(response, university_id):
        response['user']['universityId'] = university_id

        return response


class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()

            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Failed to logout: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
