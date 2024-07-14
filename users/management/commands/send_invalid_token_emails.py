from django.core.management.base import BaseCommand, CommandParser

from users.models import UserToken, CustomUser, UniversityUser
from users.password import Password

class Command(BaseCommand):
    help = "Send email for all invalid trieds tokens"

    def handle(self, *args, **options) -> None:
        users = UserToken.objects.get_user_users_waiting_to_send_email()

        if not users:
            print('Nenhum usuário para mandar email', flush = True)
        else:
            print('--------------------------------')
            
        for user in users:
            if user.account_password_status == 'first_access':
                if isinstance(user, CustomUser) and not isinstance(user, UniversityUser):
                    user = UniversityUser.objects.get(id = user.id)
                        
                Password.start_first_access_password_process(user)
            elif user.account_password_status == 'admin_reset':
                Password.start_reset_password_by_admin_process(user.email)
            elif user.account_password_status == 'user_reset':
                Password.start_reset_password_process(user.email)