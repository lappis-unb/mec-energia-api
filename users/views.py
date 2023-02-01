from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from universities.models import ConsumerUnit

from .models import CustomUser, UniversityUser
from .serializers import RetrieveUniversityUserSerializer, UniversityUserSerializer, FavoriteConsumerUnitActionSerializer, CustomUserSerializer
from .requests_permissions import RequestsPermissions


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UniversityUsersViewSet(ModelViewSet):
    queryset = UniversityUser.objects.all()
    serializer_class = UniversityUserSerializer

    def create(self, request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.defaut_users_permissions

        body_university_id = request.data['university']

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, body_university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)
            
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveUniversityUserSerializer
        return UniversityUserSerializer

    @swagger_auto_schema(request_body=FavoriteConsumerUnitActionSerializer)
    @action(detail=True, methods=['post'], url_path='favorite-consumer-units')
    def add_or_remove_favorite_consumer_unit(self, request: Request, pk=None):
        params_serializer = FavoriteConsumerUnitActionSerializer(data=request.data)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = params_serializer.validated_data
        consumer_unit_id = data['consumer_unit_id']
        action = data['action']
        user: UniversityUser = self.get_object()

        try:
            user.add_or_remove_favorite_consumer_unit(consumer_unit_id, action)
        except ConsumerUnit.DoesNotExist:
            return Response({'errors': ['Consumer unit not found']}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'errors': e.args}, status=status.HTTP_403_FORBIDDEN)

        return Response(data)
