
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.tokens import default_token_generator

from utils.endpoints_util import EndpointsUtils
from utils.user.authentication import generate_link_to_reset_password, generate_random_password
from utils.email.send_email import send_email_first_access_password, send_email_reset_password, send_email_reset_password_by_admin

from .models import UserToken, CustomUser
from .authentications import Authentication
from . import serializers

from mec_energia import settings

code_password_token_ok = 1 # Usuário tem um Password Token válido
code_password_token_expired = 2 # Email seja agendado com um novo Password Token

class Password():
    def set_password_user(user, password, is_seed_user):
        if settings.ENVIRONMENT not in ['development', 'production']:
            Password.set_and_save_user_password(user, password)
            return

        if user.type in CustomUser.university_user_types and not is_seed_user:
            Password.set_and_save_user_password(user, generate_random_password())
            Password.start_first_access_password_process(user)
        else:
            Password.set_and_save_user_password(user, password)

    def set_and_save_user_password(user, password):
        user.set_password(password)
        user.save()

    def start_reset_password_process(email):
        try:
            user = CustomUser.search_user_by_email(email = email)

            user.account_password_status = 'user_reset'
            user.save()

            token = Password._generate_password_token(user)
            link = Password.generate_link_to_reset_password(user, token, 'user_reset')
            
            send_email_reset_password(user.first_name, user.email, link)
        except Exception as error:
            raise Exception('Send email reset password: ' + str(error))

    def start_reset_password_by_admin_process(email):
        try:
            user = CustomUser.search_user_by_email(email = email)
            
            user.account_password_status = 'admin_reset'
            user.save()

            Password.set_and_save_user_password(user, generate_random_password())

            Authentication._invalid_sessions_tokens(user)

            token = Password._generate_password_token(user)
            link = Password.generate_link_to_reset_password(user, token, 'admin_reset')
            
            send_email_reset_password_by_admin(user.first_name, user.email, link)
        except Exception as error:
            raise Exception('Send email reset password: ' + str(error))

    def start_first_access_password_process(user):
        try:
            user.account_password_status = 'first_access'
            user.save()

            token = Password._generate_password_token(user)
            link = Password.generate_link_to_reset_password(user, token, 'first_access')
            
            send_email_first_access_password(user.first_name, user.university.acronym, user.email, link)
        except Exception as error:
            raise Exception('Send email first access password: ' + str(error))

    def generate_link_to_reset_password(user: str, token: str or None, password_status: str):
        if not token:
            raise Exception('Is necessary a password token')

        Password._get_user_by_token(token)

        return generate_link_to_reset_password(token, user.first_name, password_status)

    def check_password_token_is_valid(user, token):
        return default_token_generator.check_token(user, token)

    def change_user_password(user_new_password, token):
        try:
            user = Password._get_user_by_token(token)

            user.change_user_password_by_reset_password_token(user_new_password, token)
            user.set_account_password_status_to_ok()

            Password._invalid_all_generated_password_tokens(user)
        except Exception as error:
            raise Exception('Change user password: ' + str(error))
        
    def _generate_password_token(user):
        Password._invalid_all_generated_password_tokens(user)
        
        token = default_token_generator.make_token(user = user)
        UserToken.objects.create(user = user, token = token)

        return token
    
    def _get_user_by_token(token):
        return UserToken.get_user_by_token(token)

    def _invalid_all_generated_password_tokens(user):
        UserToken.objects.filter(user=user).delete()


class ResetPasswordByAdmin(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_user = request.user

        if request_user.type not in ['super_user', 'university_admin']:
            raise Exception('Esse usuário não tem permissão para executar essa ação')

        user_id = int(request.GET.get('user_id'))
        user_for_reset = CustomUser.search_user_by_id(user_id)

        if request_user.id == user_for_reset.id:
            raise Exception('Utilize o esqueci minha senha')
        
        Password.send_email_reset_password_by_admin(user_for_reset.email)

        return Response({"message": "Enviado"})


@authentication_classes([])
@permission_classes([])
class ResetPassword(generics.GenericAPIView):
    @swagger_auto_schema(query_serializer=serializers.ResetPasswordParamsSerializer,
                         responses={200: serializers.ResetPasswordParamsForDocs})
    def post(self, request, *args, **kwargs):
        try:
            request_user_email = request.GET.get('email')

            Password.send_email_reset_password(request_user_email)

            response = EndpointsUtils.create_message_endpoint_response(
                        status = EndpointsUtils.status_success, 
                        message = "O email foi enviado para o usuário com link de redefinição de senha")

            return Response(response, status.HTTP_200_OK)
        except Exception as error:
            response = EndpointsUtils.create_message_endpoint_response(
                        status = EndpointsUtils.status_error,
                        message = str(error))

            return Response(response, status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        try:
            request_token = request.GET.get('token')

            user, code_token = UserToken.get_user_by_token_and_set_invalid_tried(request_token)
            
            response = {
                "status": EndpointsUtils.status_success,
                "code": code_token,
                "message": "Token válido" if code_token == code_password_token_ok else "Novo email será enviado",
                "email": user.email,
            }
                
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([])
@permission_classes([])
class ConfirmResetPassword(generics.GenericAPIView):
    @swagger_auto_schema(request_body=serializers.ConfirmPasswordBodySerializer,
                         responses={200: serializers.ResetPasswordParamsForDocs})
    def post(self, request, *args, **kwargs):
        try:
            request_user_new_password = request.data['user_new_password']
            request_user_reset_password_token = request.data['user_token']

            Password.change_user_password(request_user_new_password, request_user_reset_password_token)

            response = EndpointsUtils.create_message_endpoint_response(
                        status = EndpointsUtils.status_success, 
                        message = "User password has been changed")

            return Response(response, status.HTTP_200_OK)
        except Exception as error:
            response = EndpointsUtils.create_message_endpoint_response(
                        status = EndpointsUtils.status_error,
                        message = str(error))

            return Response(response, status.HTTP_400_BAD_REQUEST)
