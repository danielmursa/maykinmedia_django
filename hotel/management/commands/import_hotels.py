import logging
from django.core.management.base import BaseCommand
from hotel.utils import import_hotels

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    A Django management command to import hotels from an external API.
    This command utilizes the `import_hotels` function from the utils module to fetch and import hotel data.
    """

    help = "Fetches and imports hotel data from an external API, providing success or error feedback."

    def handle(self, *args, **options):
        """
        Handle the command execution.

        This method calls the `import_hotels` function and captures its output.
        Depending on the result, it writes a success or error message to the console.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.

        Returns:
            None
        """
        logger.debug("Start import_hotels")
        success, result = import_hotels()
        if success:
            self.stdout.write(self.style.SUCCESS(f"Import successful: {result}"))
        else:
            self.stderr.write(self.style.ERROR(f"Import error: {result}"))
        logger.debug("Start import_hotels")
