from typing import Any

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import AccessToken

from .models import User

COOKIE_NAME = settings.AUTH_REFRESH_COOKIE_NAME


def get_refresh_from_client(client: APIClient) -> str:
    return str(client.cookies[COOKIE_NAME].value)


def assert_refresh_cookie_set(
    response: Response, refresh_token: str | None = None
) -> None:
    assert COOKIE_NAME in response.cookies
    cookie = response.cookies[COOKIE_NAME]

    assert cookie.value
    assert cookie["httponly"] is True
    assert cookie["samesite"] == settings.AUTH_REFRESH_COOKIE_SAMESITE
    assert cookie["path"] == settings.AUTH_REFRESH_COOKIE_PATH
    assert int(cookie["max-age"]) == int(
        api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()
    )

    if refresh_token is not None:
        assert cookie.value == refresh_token


def assert_refresh_cookie_cleared(response: Response) -> None:
    assert COOKIE_NAME in response.cookies
    cookie = response.cookies[COOKIE_NAME]

    assert cookie.value == ""
    assert cookie["max-age"] == 0


@pytest.mark.django_db
def test_create_user() -> None:
    user = User.objects.create_user(
        email="test@test.com",
        password="testpassword",
    )
    assert user.email == "test@test.com"
    assert user.check_password("testpassword")


@pytest.mark.django_db
def test_api_register(api_client: APIClient, register_data: dict[str, str]) -> None:
    response = api_client.post(reverse("accounts:register"), register_data)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert "access" in response_data
    assert "refresh" not in response_data
    assert response_data["token_type"] == "Bearer"

    access = AccessToken(response_data["access"])
    assert int(access["user_id"]) == User.objects.get(email=register_data["email"]).id

    refresh_token = get_refresh_from_client(api_client)
    assert_refresh_cookie_set(response, refresh_token)


@pytest.mark.django_db
def test_api_register_incorrect(api_client: APIClient) -> None:
    bad_email_data = {
        "username": "testuser",
        "email": "bad-email",
        "password": "testpass123",
    }
    response = api_client.post(reverse("accounts:register"), bad_email_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert COOKIE_NAME not in response.cookies

    bad_password_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "",
    }
    response = api_client.post(reverse("accounts:register"), bad_password_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert COOKIE_NAME not in response.cookies


@pytest.mark.django_db
def test_api_login(api_client: APIClient) -> None:
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
    assert "refresh" not in response_data
    assert response_data["token_type"] == "Bearer"

    refresh_token = get_refresh_from_client(api_client)
    assert_refresh_cookie_set(response, refresh_token)


@pytest.mark.django_db
def test_api_login_incorrect(api_client: APIClient) -> None:
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword",
    }
    response = api_client.post(reverse("accounts:token_obtain_pair"), login_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response_data
    assert COOKIE_NAME not in response.cookies


@pytest.mark.django_db
def test_refresh_returns_access_from_cookie(
    registered_client: tuple[APIClient, Any, str],
) -> None:
    client, _, refresh = registered_client

    response = client.post(reverse("accounts:token_refresh"))
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response_data
    assert "refresh" not in response_data
    # Sin rotación la cookie no se vuelve a enviar ni cambia.
    assert COOKIE_NAME not in response.cookies
    assert get_refresh_from_client(client) == refresh


@pytest.mark.django_db
def test_refresh_without_cookie(api_client: APIClient) -> None:
    response = api_client.post(reverse("accounts:token_refresh"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()
    assert COOKIE_NAME not in response.cookies


@pytest.mark.django_db
def test_refresh_with_invalid_cookie(api_client: APIClient) -> None:
    api_client.cookies[COOKIE_NAME] = "not-a-valid-token"

    response = api_client.post(reverse("accounts:token_refresh"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()
    assert_refresh_cookie_cleared(response)


@pytest.mark.django_db
def test_refresh_after_logout_fails(
    api_client: APIClient,
    registered_client: tuple[APIClient, Any, str],
    logout_url: str,
) -> None:
    client, _, refresh = registered_client
    client.post(logout_url)

    # Simula un cliente que conserva el refresh token aunque se hizo logout.
    api_client.cookies[COOKIE_NAME] = refresh
    response = api_client.post(reverse("accounts:token_refresh"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert_refresh_cookie_cleared(response)


@pytest.mark.django_db
def test_logout_revokes_refresh_token(
    registered_client: tuple[APIClient, Any, str],
    api_client: APIClient,
    logout_url: str,
) -> None:
    client, _, refresh = registered_client

    response = client.post(logout_url)

    assert response.status_code == status.HTTP_200_OK
    assert BlacklistedToken.objects.count() == 1
    assert_refresh_cookie_cleared(response)

    api_client.cookies[COOKIE_NAME] = refresh
    refresh_response = api_client.post(reverse("accounts:token_refresh"))
    assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_logout_does_not_require_access_token(
    registered_client: tuple[APIClient, Any, str], logout_url: str
) -> None:
    client, _, _ = registered_client

    # El cliente no envía cabecera Authorization, solo la cookie.
    response = client.post(logout_url)

    assert response.status_code == status.HTTP_200_OK
    assert BlacklistedToken.objects.count() == 1


@pytest.mark.django_db
def test_logout_without_cookie(api_client: APIClient, logout_url: str) -> None:
    response = api_client.post(logout_url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert BlacklistedToken.objects.count() == 0


@pytest.mark.django_db
def test_logout_with_invalid_refresh(api_client: APIClient, logout_url: str) -> None:
    api_client.cookies[COOKIE_NAME] = "not-a-valid-token"

    response = api_client.post(logout_url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert BlacklistedToken.objects.count() == 0
    assert_refresh_cookie_cleared(response)


@pytest.mark.django_db
def test_logout_twice(
    registered_client: tuple[APIClient, Any, str], logout_url: str
) -> None:
    client, _, _ = registered_client

    first = client.post(logout_url)
    second = client.post(logout_url)

    assert first.status_code == status.HTTP_200_OK
    assert second.status_code == status.HTTP_400_BAD_REQUEST
    assert BlacklistedToken.objects.count() == 1
    assert_refresh_cookie_cleared(second)
