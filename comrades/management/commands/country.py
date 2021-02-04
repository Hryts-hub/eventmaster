from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
import requests

from comrades.models import Country


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://www.officeholidays.com/countries"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        arr = [i for i in soup.find_all("div", {"class": "four omega columns"})]
        arr_country = [[j.text.strip() for j in i.find_all("a")] for i in arr]
        list_country = []
        [[list_country.append(j) for j in arr_country[i]] for i in range(0, len(arr_country))]

        arr_slug = [i.find_all("a") for i in arr]
        list_slug = []
        [[list_slug.append(j) for j in arr_slug[i]] for i in range(0, len(arr_slug))]
        slugs = [str(list_slug[i]).split('/countries/')[1].split('"')[0] for i in range(0, len(list_slug))]

        country_fields = [
            Country(slug=slugs[i], country_name=list_country[i])
            for i in range(0, len(slugs))
        ]

        Country.objects.bulk_create(country_fields)

        # for country in tqdm(all_arr):
        #     Country.objects.create(name=country)
