from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from comrades.models import CustomUser, Country
from events.models import Holidays


class RestTest(APITestCase):
    def setUp(self):
        self.country_obj = Country.objects.create(
            slug="belarus",
            country_name="Belarus",
        )
        # праздник с страной, внимательно с полями, они д.б. как в базе, иначе код упадет
        Holidays.objects.create(
            holiday="Belarus: test1",
            country=Country.objects.get(slug="belarus"),
            date="2021-05-09",
            duration="1 day, ",
            description="xxxxxxxx"
        )
        # юзер с страной
        self.user = CustomUser.objects.create_user(
            email="bbpedro@gmail.com",
            username="bbpedro",
            password="useruser",
            first_name="pedro",
            last_name="pedro",
            country=Country.objects.get(slug="belarus"),
            offset="3",
            )
        url = reverse("login")
        # valid data, login by email
        data5 = {
            'login': "bbpedro@gmail.com",
            'password': "useruser",
        }
        response = self.client.post(
            path=url,
            data=data5,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client = APIClient()
        self.token = Token.objects.get(user__username='bbpedro')
        self.headers = {"Authorization": f"Token {self.token}"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # events for tests

        # "test EVENT-1"
        url = reverse("list_create_event")
        data = {
            "event": "test EVENT-1",
            "date_event": "2021-08-08",
            "start_time": "11:00",
            "end_time": "12:00",
            "remind": "3600",
        }
        response = self.client.post(
            url,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # "test EVENT-2"
        url = reverse("list_create_event")
        data = {
            "event": "test EVENT-2",
            "date_event": "2021-08-08",
            "start_time": "14:00",
            "end_time": "16:00",
            "remind": "86400",
        }
        response = self.client.post(
            url,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # "test EVENT-3"
        url = reverse("list_create_event")
        data = {
            "event": "test EVENT-3",
            "date_event": "2021-08-07",
            "start_time": "15:00",
            "end_time": "16:00",
            "remind": "604800",
        }
        response = self.client.post(
            url,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_create_event(self):
        url = reverse("list_create_event")
        response = self.client.get(
            url,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # event without remind
        data = {
            "event": "test AAAAAA",
            "date_event": "2021-08-08",
            "start_time": "11:00",
            "end_time": "12:00",
            "remind": "0",
        }
        response = self.client.post(
            url,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # event with remind in the past
        data = {
            "event": "test PAST",
            "date_event": "2021-01-01",
            "start_time": "11:00",
            "end_time": "12:00",
            "remind": "604800",
        }
        response = self.client.post(
            url,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['message'],
            "You create the event with remind in the past - we can't remind you about this event by email"
        )
        print("test_list_create_event")

    def test_statistic_by_user(self):
        url = reverse("statistic_by_user")
        response = self.client.get(
            url,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        print("test_statistic_by_user")

    def test_statistic_day(self):
        url = reverse("statistic_day")
        data = {
            "date_event": "2021-08-08",
        }
        response = self.client.get(
            url,
            headers=self.headers,
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # There are 2 events in request day
        self.assertEqual(len(response.data['2021-08-08'][0]), 2)
        print("test_statistic_day")

    def test_statistic_month(self):
        url = reverse("statistic_month")
        data = {
            "month": "2021-08",
        }
        response = self.client.get(
            url,
            headers=self.headers,
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # There are 2 days with events
        self.assertEqual(len(response.data), 2)
        print("test_statistic_month")

    def test_holidays_month(self):
        # holiday in belarus 2021-05-09
        url = reverse("holidays_month")
        data = {
            "month": "2021-05",
        }
        response = self.client.get(
            url,
            headers=self.headers,
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # in test base our country have only 1 day with holiday
        self.assertEqual(len(response.data), 1)
        print("test_holidays_month")

