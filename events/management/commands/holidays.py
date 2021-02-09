from django.core.management import BaseCommand
from events.services import create_holidays


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        create_holidays()
