from django.core.management.base import BaseCommand
from events.services import get_countries
from comrades.models import Country


class Command(BaseCommand):
    def handle(self, *args, **options):
        slugs, list_country = get_countries()
        country_fields = [
            Country(slug=slugs[i], country_name=list_country[i])
            for i in range(0, len(slugs))
        ]
        Country.objects.bulk_create(country_fields)

