from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


# Create your tests here.
class AuthTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.register_data = {
            "username": "david",
            "email": "david@david.com",
            "password": "david1331",
        }
        self.register_data_bad_email = {
            "username": "david",
            "email": "david-hola",
            "password": "david1331",
        }

        self.register_data_bad_username = {
            "username": "",
            "email": "david@david.com",
            "password": "david1331",
        }

        self.register_data_bad_password = {
            "username": "david",
            "email": "david@david.com",
            "password": "",
        }

        self.login_data = {
            "username": "david",
            "password": "david1331",
        }

        self.login_data_error = {
            "username": "david2",
            "password": "123456",
        }

    def test_register(self):
        response = self.client.post(reverse("register"), data=self.register_data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response_data)

    def test_resgister_incorrect(self):
        response = self.client.post(
            reverse("register"), data=self.register_data_bad_email
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            reverse("register"), data=self.register_data_bad_username
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            reverse("register"), data=self.register_data_bad_password
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        # first register the user
        self.client.post(reverse("register"), data=self.register_data)
        # user login
        response = self.client.post(reverse("login"), data=self.login_data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response_data)

    def test_login_incorrect(self):
        # with data not exists
        response = self.client.post(reverse("login"), data=self.login_data_error)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response_data)

    def test_logout(self):
        # user register
        self.client.post(reverse("register"), data=self.register_data)
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh_token", response.cookies)
        self.assertEqual(response.cookies["refresh_token"].value, "")

    def test_new_access_token(self):
        # user register
        self.client.post(reverse("register"), data=self.register_data)

        response = self.client.get(reverse("new_access_token"))
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response_data)

    def test_new_access_token_incorrect(self):
        # register
        self.client.post(reverse("register"), data=self.register_data)
        # delate cookies
        self.client.cookies.clear()

        response = self.client.get(reverse("new_access_token"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
