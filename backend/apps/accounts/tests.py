import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

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
    response = api_client.post(reverse("accounts:register"), register_data)
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
    response = api_client.post(reverse("accounts:register"), bad_email_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    bad_password_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "",
    }
    response = api_client.post(reverse("accounts:register"), bad_password_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_api_login(api_client):
    register_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "loginpass123",
    }
    api_client.post(reverse("accounts:register"), register_data)

    login_data = {
        "email": "login@example.com",
        "password": "loginpass123",
    }
    response = api_client.post(reverse("accounts:token_obtain_pair"), login_data)
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
    response = api_client.post(reverse("accounts:token_obtain_pair"), login_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response_data


@pytest.mark.django_db
def test_logout_revokes_refresh_token(registered_client, api_client):
    client, access, refresh = registered_client
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    response = client.post(reverse("accounts:logout"), {"refresh": refresh})

    assert response.status_code == status.HTTP_200_OK
    assert BlacklistedToken.objects.count() == 1

    refresh_response = api_client.post(
        reverse("accounts:token_refresh"), {"refresh": refresh}
    )
    assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_logout_requires_authentication(api_client, registered_client):
    _, _, refresh = registered_client

    response = api_client.post(reverse("accounts:logout"), {"refresh": refresh})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert BlacklistedToken.objects.count() == 0


@pytest.mark.django_db
def test_logout_with_invalid_refresh(authenticated_client):
    response = authenticated_client.post(
        reverse("accounts:logout"), {"refresh": "not-a-valid-token"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert BlacklistedToken.objects.count() == 0


@pytest.mark.django_db
def test_logout_twice(registered_client):
    client, access, refresh = registered_client
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    url = reverse("accounts:logout")

    first = client.post(url, {"refresh": refresh})
    second = client.post(url, {"refresh": refresh})

    assert first.status_code == status.HTTP_200_OK
    assert second.status_code == status.HTTP_400_BAD_REQUEST
    assert BlacklistedToken.objects.count() == 1
