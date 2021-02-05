from rest_framework.authentication import TokenAuthentication
from rest_framework.test import APITestCase, RequestsClient, APIClient
from django.urls import reverse
from rest_framework import status
from json import dumps
from rest_framework.authtoken.models import Token
from comrades.models import CustomUser, Country
from events.models import Events


class RestTest(APITestCase):
    def setUp(self):
        self.country_obj = Country.objects.create(
            slug="belarus",
            country_name="Belarus",
        )
        # нужно сделать юзера с страной
        self.user = CustomUser.objects.create_user(
            email="bbpedro@gmail.com",
            username="bbpedro",
            password="useruser",
            first_name="pedro",
            last_name="pedro",
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

        url = reverse("list_create_event")
        data = {
            "event": "test EVENT-1",
            "date_event": "2021-08-08",
            "start_time": "11:00",
            "end_time": "12:00",
        }
        response = self.client.post(
            url,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.test_response1 = response.data

    # def test_token(self):
    #     print(self.token)

    def test_list_create_event(self):
        url = reverse("list_create_event")
        response = self.client.get(
            url,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            "event": "test AAAAAA",
            "date_event": "2021-08-08",
            "start_time": "11:00",
            "end_time": "12:00",
        }
        response = self.client.post(
            url,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_statistic_by_user(self):
        url = reverse("statistic_by_user")
        response = self.client.get(
            url,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def holidays_month(self):
        # у тестового юзера пока что нет страны. так что...
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

