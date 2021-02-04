from tqdm import tqdm
from django.core.management import BaseCommand
from ics import Calendar
import requests

from comrades.models import Country
from events.models import Holidays


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        i = 0
        k = 0
        m = 0
        for country in tqdm(countries):
            url = f"https://www.officeholidays.com/ics/ics_country.php?tbl_country={country}"
            res = requests.get(url).text
            k += 1
            try:

                calendar = Calendar(res)
                holidays = calendar.events
                for holiday_obj in holidays:
                    i += 1
                    print()
                    print(k, i)
                    # print(holiday_obj)
                    # print(holiday_obj.name)
                    # print(holiday_obj.begin.date())
                    # print(holiday_obj.end.date())
                    # print(holiday_obj.description)
                    # print(holiday_obj.location)
                    # print(holiday_obj.duration)

                    Holidays.objects.create(
                        holiday=holiday_obj.name,
                        country=Country.objects.get(country_name=holiday_obj.location),
                        # date=holiday_obj.begin.date(),
                        date=holiday_obj.begin.format("YYYY-MM-DD"),
                        duration=holiday_obj.duration,
                        description=holiday_obj.description,
                        )
            except Exception as e:
                print("-----------------------------------------------------------------------")
                m += 1
                print(k, i, m)
                print(e)
                print()
                pass

            # k = 222 country, i = 4770 holiday, m = 64 mistakes, 3738 - total holidays in bd