from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Django management command to create a superuser with default values.

    This command creates a Django superuser with a predefined username, email,
    and password if one does not already exist with the specified username.
    The default values are:
        - Username: "admin"
        - Email: "admin@admin.com"
        - Password: "admin"

    Example usage:
        python manage.py createsuperuser_custom
    """

    help = "Creates a superuser with default values"

    def handle(self, *args, **kwargs):
        # Default values
        username = "admin"
        email = "admin@admin.com"
        password = "admin"

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Superuser with username "{username}" already exists.'
                )
            )
            return

        User.objects.create_superuser(username, email, password)
        self.stdout.write(
            self.style.SUCCESS(f'Superuser "{username}" created successfully.')
        )
