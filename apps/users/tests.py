import pytest
from django.urls import reverse
from rest_framework import status
from .models import User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="test@test.com",
        password="testpassword",
    )
    assert user.email == "test@test.com"
    assert user.check_password("testpassword")


@pytest.mark.django_db
def test_api_register(api_client, register_data):
    response = api_client.post(reverse("api_register"), register_data)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert "access" in response_data
    assert "refresh" in response_data


@pytest.mark.django_db
def test_api_register_incorrect(api_client):
    bad_email_data = {
        "username": "testuser",
        "email": "bad-email",
        "password": "testpass123",
    }
    response = api_client.post(reverse("api_register"), bad_email_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    bad_password_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "",
    }
    response = api_client.post(reverse("api_register"), bad_password_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_api_login(api_client):
    register_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "loginpass123",
    }
    api_client.post(reverse("api_register"), register_data)

    login_data = {
        "email": "login@example.com",
        "password": "loginpass123",
    }
    response = api_client.post(reverse("api_token_obtain_pair"), login_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response_data
    assert "refresh" in response_data


@pytest.mark.django_db
def test_api_login_incorrect(api_client):
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword",
    }
    response = api_client.post(reverse("api_token_obtain_pair"), login_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response_data
