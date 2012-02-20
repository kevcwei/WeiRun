from django.core.management.base import BaseCommand
from main.models import User

class Command(BaseCommand):
    """A cron job command that's supposed to be run periodically."""

    def handle(self, *args, **options):
        self.stdout.write("This is just a test job.\n")
