
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    # management/commands/createsuperuser_custom.py
    help = 'Creates a superuser with default values'

    def handle(self, *args, **kwargs):
        # Default values
        username = 'admin'
        email = 'admin@admin.com'
        password = 'admin'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superuser with username "{username}" already exists.'))
            return

        User.objects.create_superuser(username, email, password)
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
