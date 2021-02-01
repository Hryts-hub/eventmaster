from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from json import dumps
from rest_framework.authtoken.models import Token
from comrades.models import CustomUser


class RestTest(APITestCase):
    def setUp(self):
        self.url = reverse('registration')
        self.user = CustomUser.objects.create_user(
            email="bbpedro@gmail.com",
            username="bbpedro",
            password="useruser",
            first_name="pedro",
            last_name="pedro",
            )
        # self.user = CustomUser.objects.get(
        #     email="bbpedro@gmail.com"
        # )

    def test_registration(self):
        url = reverse('registration')
        # valid data
        data = {
            'email': "pedro@gmail.com",
            'username': "pedro",
            'password': "useruser",
            'first_name': "pedro",
            'last_name': "pedro",
            'country': "",
        }
        # invalid field name
        data1 = {
            'eemail': "pedro@gmail.com",
            'username': "pedro",
            'password': "useruser",
            'first_name': "pedro",
            'last_name': "pedro",
            'country': "",
        }
        # invalid username
        data2 = {
            'email': "pedro@gmail.com",
            'username': "pedro@",
            'password': "useruser",
            'first_name': "pedro",
            'last_name': "pedro",
            'country': "",
        }
        # invalid email
        data3 = {
            'email': "pedrogmail.com",
            'username': "pedro",
            'password': "useruser",
            'first_name': "pedro",
            'last_name': "pedro",
            'country': "",
        }
        # invalid fields number
        data4 = {
            'email': "pedro@gmail.com",
            'username': "pedro",
            'password': "useruser",
        }
        # invalid data
        data5 = {
            'email': "pedro@gmail.com",
            'username': "pedro",
            'password': "useruser",
            'first_name': "pedro",
            'last_name': "",
            'country': "",
        }

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.post(
            path=url,
            data=dumps(data1),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            path=url,
            data=dumps(data2),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            path=url,
            data=dumps(data3),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            path=url,
            data=dumps(data4),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            path=url,
            data=dumps(data5),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            path=url,
            data=dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # try create user, that already exists
        response = self.client.post(
            path=url,
            data=dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activation(self):
        url = reverse('registration')
        # valid data
        data = {
            'email': "pedro@gmail.com",
            'username': "pedro",
            'password': "useruser",
            'first_name': "pedro",
            'last_name': "pedro",
            'country': "",
        }
        response = self.client.post(
            path=url,
            data=dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        activation_link = response.json()["activation_link"]
        webtoken = response.json()["webtoken"]
        # valid data
        data = {
            "login": "pedro@gmail.com",
            "webtoken": webtoken
        }
        # invalid field
        data1 = {
            "lo0gin": "pedro@gmail.com",
            "webtoken": webtoken
        }
        # invalid login
        data2 = {
            "lo0gin": "wwwwwwwpedro@gmail.com",
            "webtoken": webtoken
        }
        # invalid webtoken
        data3 = {
            "lo0gin": "wwwwwwwpedro@gmail.com",
            "webtoken": "12345"
        }
        # invalid login by username
        data4 = {
            "lo0gin": "pedrooooo",
            "webtoken": webtoken
        }
        response = self.client.get(activation_link, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.post(
            path=activation_link,
            data=dumps(data1),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            path=activation_link,
            data=dumps(data2),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            path=activation_link,
            data=dumps(data3),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            path=activation_link,
            data=dumps(data4),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # login by email
        response = self.client.post(
            path=activation_link,
            data=dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        # login by username
        data = {
            "login": "pedro",
            "webtoken": webtoken
        }
        response = self.client.post(
            path=activation_link,
            data=dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_login(self):
        url = reverse("login")
        # invalid field name
        data1 = {
            'leogin': "bbpedro@gmail.com",
            'password': "useruser",
        }
        # invalid field number
        data2 = {
            'login': "bbpedro@gmail.com",
        }
        # email does not exist
        data3 = {
            'login': "wbpedro@gmail.com",
            'password': "useruser",
        }
        # username does not exist
        data4 = {
            'login': "wbpedro",
            'password': "useruser",
        }
        # valid data, login by email
        data6 = {
            'login': "bbpedro@gmail.com",
            'password': "useruser",
        }
        # valid data, login by username
        data7 = {
            'login': "bbpedro",
            'password': "useruser",
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.post(
            path=url,
            data=dumps(data1),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            path=url,
            data=dumps(data2),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            path=url,
            data=dumps(data3),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(
            path=url,
            data=dumps(data4),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(
            path=url,
            data=dumps(data6),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            path=url,
            data=dumps(data7),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        url = reverse("logout")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.post(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token(self):
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
        self.assertEqual(
            Token.objects.get(user=self.user).__str__(),
            response.json()
        )


# coverage run --source="." manage.py test
# coverage html