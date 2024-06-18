from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from mec_energia import settings

from universities.models import ConsumerUnit, University

from .managers import CustomUserManager


class UserToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Token for {self.user.username}'


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    
    ### User types
    super_user_type = 'super_user'
    university_admin_user_type = 'university_admin'
    university_user_type = 'university_user'

    all_user_types = [
        super_user_type,
        university_admin_user_type,
        university_user_type
    ]

    university_user_types = [
        university_admin_user_type,
        university_user_type
    ]

    user_types = (
        (super_user_type, 'super_user'),
        (university_admin_user_type, 'university_admin'),
        (university_user_type,'university_user'),
    )

    username = None
    
    first_name = models.CharField(
        max_length=25
    )

    last_name = models.CharField(
        max_length=25
    )

    email = models.EmailField(
        _('Email is required'),
        unique=True,
        null=False
    )

    type = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        choices=user_types
    )

    password_status = (
        ('OK', 'OK'),
        ('first_access', 'first_access'),
        ('admin_reset', 'admin_reset'),
        ('user_reset', 'user_reset'),
    )

    account_password_status = models.CharField(
        default='OK',
        max_length=25,
        null=False,
        blank=False,
        choices=password_status
    )

    is_seed_user = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @classmethod
    def search_user_by_id(cls, id):
        try:
            user = cls.objects.get(id = id)

            return user
        except ObjectDoesNotExist:
            raise Exception('User does not exist')

    @classmethod
    def search_user_by_email(cls, email):
        try:
            user = cls.objects.get(email = email)

            return user
        except ObjectDoesNotExist:
            raise Exception('User does not exist')

    def change_user_password_by_reset_password_token(self, new_password, reset_password_token):
        from .authentications import Password

        try:
            if Password.check_password_token_is_valid(self, reset_password_token):
                self.set_password(new_password)
                self.save()
            else:
                raise Exception('Reset password token is not valid')

            return self
        except Exception as error:
            raise Exception(str(error))
        
    def set_account_password_status_to_ok(self):
        self.account_password_status = 'OK'
        self.save()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} [{self.email}]'


class UniversityUser(CustomUser):
    university_admin_user_type = CustomUser.university_admin_user_type
    university_user_type = CustomUser.university_user_type

    favorite_consumer_units = models.ManyToManyField(ConsumerUnit, blank=True)
    
    university = models.ForeignKey(
        University,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        verbose_name='Universidade',
        help_text=_(
            'Um Usuário de Universidade deve estar ligado a uma Universidade')
    )

    def add_or_remove_favorite_consumer_unit(self, consumer_unit_id: int | str, action: str):
        unit = ConsumerUnit.objects.get(pk=consumer_unit_id)

        if unit.university.id != self.university.id:
            raise Exception('Cannot add/remove consumer unit from another university')

        if action == 'add':
            self.favorite_consumer_units.add(unit)
        elif action == 'remove':
            self.favorite_consumer_units.remove(unit)
        else:
            raise Exception('"action" field must be "add" or "remove"')

    def get_user_favorite_consumer_units(self):
        return self.favorite_consumer_units.all()
    
    def check_if_consumer_unit_is_your_favorite(self, consumer_unit_id):
        favorite_consumer_units = self.get_user_favorite_consumer_units()

        if favorite_consumer_units.filter(id = consumer_unit_id):
            return True
        
        return False

    def change_university_user_type(self, new_user_type):
        if not new_user_type in CustomUser.university_user_types:
            raise Exception('New University User type does not exist')
        
        if not self.type in CustomUser.university_user_types:
            raise Exception('User is not User University')
        
        if self.type == CustomUser.university_admin_user_type:
            admin_university_users = UniversityUser.objects.all().filter(university = self.university, type = CustomUser.university_admin_user_type)
            
            if len(admin_university_users) == 1:
                raise Exception('This User is the last Admin University User')
        
        self.type = new_user_type
        self.save()
