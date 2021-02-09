from django.core.management.base import BaseCommand
from events.services import create_country


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_country()

