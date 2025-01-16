from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from unittest.mock import patch
from .models import CodeToConfirm


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

    @patch("authentication.views.send_confirm_email")
    def test_register(self, mock_send_confirm_email):
        mock_send_confirm_email.return_value = None

        response = self.client.post(reverse("register"), self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(mock_send_confirm_email, "send_confirm_email wast not called")

        args, kwargs = mock_send_confirm_email.call_args
        self.code = kwargs.get("code")

        code = CodeToConfirm.objects.filter(code=self.code).first()
        self.assertIsNotNone(code, f"Code {self.code} not found in the database")
        self.assertEqual(code.code, self.code)

    def test_register_incorrect(self):
        response = self.client.post(reverse("register"), self.register_data_bad_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            reverse("register"), data=self.register_data_bad_username
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            reverse("register"), data=self.register_data_bad_password
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("authentication.views.send_confirm_email")
    def test_confirm_email(self, mock_send_confirm_email):
        mock_send_confirm_email.return_value = None
        response = self.client.post(reverse("register"), self.register_data)
        code = CodeToConfirm.objects.first().code

        response = self.client.post(reverse("confirm_email"), {"code": f"{code}"})
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response_data)

    def test_confirm_email_incorrect(self):
        # without code
        response = self.client.post(reverse("confirm_email"), {"code": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # code do not exist
        response = self.client.post(reverse("confirm_email"), {"code": "852456"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("authentication.views.send_confirm_email")
    def test_login(self, mock_send_confirm_email):
        mock_send_confirm_email.return_value = None

        self.client.post(reverse("register"), self.register_data)
        code = CodeToConfirm.objects.first().code

        self.client.post(reverse("confirm_email"), {"code": f"{code}"})

        response = self.client.post(reverse("login"), self.login_data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response_data)

    def test_login_incorrect(self):
        # with data not exists
        response = self.client.post(reverse("login"), data=self.login_data_error)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response_data)

    @patch("authentication.views.send_confirm_email")
    def test_logout(self, mock_send_confirm_email):
        mock_send_confirm_email.return_value = None
        # user register
        self.client.post(reverse("register"), data=self.register_data)
        code = CodeToConfirm.objects.first().code
        self.client.post(reverse("confirm_email"), {"code": f"{code}"})

        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh_token", response.cookies)
        self.assertEqual(response.cookies["refresh_token"].value, "")

    @patch("authentication.views.send_confirm_email")
    def test_new_access_token(self, mock_send_confirm_email):
        mock_send_confirm_email.return_value = None
        # user register
        self.client.post(reverse("register"), data=self.register_data)
        code = CodeToConfirm.objects.first().code
        self.client.post(reverse("confirm_email"), {"code": f"{code}"})

        response = self.client.get(reverse("new_access_token"))
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response_data)

    @patch("authentication.views.send_confirm_email")
    def test_new_access_token_incorrect(self, mock_send_confirm_email):
        mock_send_confirm_email.return_value = None
        # user register
        self.client.post(reverse("register"), data=self.register_data)
        code = CodeToConfirm.objects.first().code
        self.client.post(reverse("confirm_email"), {"code": f"{code}"})
        # delate cookies
        self.client.cookies.clear()

        response = self.client.get(reverse("new_access_token"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch("authentication.views.send_confirm_email")
    def test_check_auth(self, mock_send_confirm_email):
        mock_send_confirm_email.return_value = None
        # user register
        self.client.post(reverse("register"), data=self.register_data)
        code = CodeToConfirm.objects.first().code
        self.client.post(reverse("confirm_email"), {"code": f"{code}"})

        response = self.client.get(reverse("check_auth"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertTrue(response_data.get("isLogged"))

    @patch("authentication.views.send_confirm_email")
    def test_check_auth_incorrect(self, mock_send_confirm_email):
        mock_send_confirm_email.return_value = None
        # user register
        self.client.post(reverse("register"), data=self.register_data)
        code = CodeToConfirm.objects.first().code
        self.client.post(reverse("confirm_email"), {"code": f"{code}"})
        self.client.cookies.clear()

        # Invalid token
        response = self.client.get(
            reverse("check_auth"), cookies={"refresh_token": "no-token"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.json()
        self.assertFalse(response_data.get("IsLogged"))

        # without token
        response = self.client.get(reverse("check_auth"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.json()
        self.assertFalse(response_data.get("IsLogged"))
        self.assertIn("detail", response_data)
