import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_register(api_client, register_data):
    response = api_client.post(reverse("register"), register_data)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert "access" in response_data
    assert "refresh" in response_data


@pytest.mark.django_db
def test_register_incorrect(api_client):
    bad_email_data = {
        "username": "testuser",
        "email": "bad-email",
        "password": "testpass123",
    }
    response = api_client.post(reverse("register"), bad_email_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    bad_username_data = {
        "username": "",
        "email": "test@example.com",
        "password": "testpass123",
    }
    response = api_client.post(reverse("register"), bad_username_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    bad_password_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "",
    }
    response = api_client.post(reverse("register"), bad_password_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login(api_client):
    register_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "loginpass123",
    }
    api_client.post(reverse("register"), register_data)

    login_data = {
        "email": "login@example.com",
        "password": "loginpass123",
    }
    response = api_client.post(reverse("token_obtain_pair"), login_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response_data
    assert "refresh" in response_data


@pytest.mark.django_db
def test_login_incorrect(api_client):
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword",
    }
    response = api_client.post(reverse("token_obtain_pair"), login_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response_data
