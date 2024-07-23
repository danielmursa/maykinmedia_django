from django.core.management.base import BaseCommand
from hotel.utils import import_cities


class Command(BaseCommand):
    """
    A Django management command to import cities from an external API.
    This command utilizes the `import_cities` function from utils module to fetch and import city data.
    """

    help = "Fetches and imports city data from an external API, providing success or error feedback."

    def handle(self, *args, **options):
        """
        Handle the command execution.

        This method calls the `import_cities` function and captures its output.
        Depending on the result, it writes a success or error message to the console.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.

        Returns:
            None
        """
        success, result = import_cities()
        if success:
            self.stdout.write(self.style.SUCCESS(f"Import successful: {result}"))
        else:
            self.stderr.write(self.style.ERROR(f"Import error: {result}"))
