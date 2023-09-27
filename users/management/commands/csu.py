from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            phone=79528532568,
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('simba2106')
        user.save()