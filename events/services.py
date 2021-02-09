from bs4 import BeautifulSoup
import requests
from comrades.models import Country
from events.models import Holidays
from tqdm import tqdm
from ics import Calendar


def create_country():
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


def create_holidays():
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
                # print()
                # print(k, i)
                Holidays.objects.create(
                    holiday=holiday_obj.name,
                    country=Country.objects.get(country_name=holiday_obj.location),
                    date=holiday_obj.begin.date(),
                    duration=holiday_obj.duration,
                    description=holiday_obj.description,
                )
        except Exception as e:
            # print("-----------------------------------------------------------------------")
            m += 1
            # print(k, i, m)
            print(e)
            # print()
            pass

        # k = 222 country, i = 4770 holiday, m = 64 mistakes, 3738 - total holidays in bd