from bs4 import BeautifulSoup
import requests
from comrades.models import Country
from events.models import Holidays
from tqdm import tqdm
from ics import Calendar


def get_countries():
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

    slugs.sort()
    list_country.sort()

    return slugs, list_country


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
                Holidays.objects.create(
                    holiday=holiday_obj.name,
                    country=Country.objects.get(country_name=holiday_obj.location),
                    date=holiday_obj.begin.date(),
                    duration=holiday_obj.duration,
                    description=holiday_obj.description,
                )
        except Exception as e:
            m += 1
            print(e)
            pass
    print(k, i, m)

    # k = 222 country, i = 4770 holidays, m = 64 mistakes, 4738 - total holidays in bd


def check_countries():
    slugs, list_country = get_countries()
    countries_in_bd = Country.objects.all()

    bd_slugs = []
    bd_list_country = []
    for country in countries_in_bd:
        bd_slugs.append(country.slug)
        bd_list_country.append(country.country_name)
    bd_slugs.sort()
    bd_list_country.sort()

    if slugs == bd_slugs and list_country == bd_list_country:
        return "List of countries without changes. "
    else:
        obj = []
        for slug in bd_slugs:
            country = Country.objects.get(slug=slug)
            country.updated = False
            obj.append(country)
        Country.objects.bulk_update(obj, ['updated'])

        for i in range(0, len(slugs)):
            Country.objects.update_or_create(slug=slugs[i], defaults={"country_name": list_country[i], "updated": True})

    deleted = Country.objects.filter(updated=False).delete()
    return f"List of countries was updated. Deleted objects: {deleted}. "


def update_holidays():
    print("Start update holidays.")
    try:
        check = check_countries()
    except Exception as e:
        check = False
        print(e)
        pass

    if check:
        count_of_deleted = 0
        countries = Country.objects.all()
        for country in tqdm(countries):
            url = f"https://www.officeholidays.com/ics/ics_country.php?tbl_country={country}"
            res = requests.get(url).text
            bd_holidays_in_country = Holidays.objects.filter(country=country.slug)
            obj = []
            try:
                for holiday_obj in bd_holidays_in_country:
                    holiday = Holidays.objects.get(id=holiday_obj.id)
                    holiday.updated = False
                    obj.append(holiday)
                bd_holidays_in_country.bulk_update(obj, ['updated'])
            except Exception as e:
                return e

            try:
                calendar = Calendar(res)
                holidays = calendar.events
                for holiday_obj in holidays:
                    Holidays.objects.update_or_create(
                        holiday=holiday_obj.name,
                        date=holiday_obj.begin.date(),
                        duration=holiday_obj.duration,
                        description=holiday_obj.description,
                        defaults={
                            "holiday": holiday_obj.name,
                            "country": Country.objects.get(country_name=holiday_obj.location),
                            "date": holiday_obj.begin.date(),
                            "duration": holiday_obj.duration,
                            "description": holiday_obj.description,
                            "updated": True
                        }
                    )
            except Exception as e:
                print(e)
                pass
            holiday_for_delete = Holidays.objects.filter(country=country.slug).filter(updated=False)
            deleted = holiday_for_delete.delete()
            count_of_deleted += deleted[0]
        print(check, f"Count of deleted holidays objects: {count_of_deleted}.")


def event_per_day_func(events):
    i = 0
    event_list = []
    ev = dict()
    for event in events:
        event_name = event.event
        start_time = event.start_time
        end_time = event.end_time
        i += 1
        ev[i] = [start_time, end_time, event_name]
    event_list.append(ev)
    return event_list
