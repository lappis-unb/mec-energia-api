from django.core.management.base import BaseCommand, CommandParser

from users.models import UserToken

class Command(BaseCommand):
    help = "Send email for all invalid trieds tokens"

    def handle(self, *args, **options) -> None:
       print('----------------', flush=True)
       token = UserToken.objects.get_invalid_tried_token()

       send_email(token.user.email)
       print('ok', flush=True)