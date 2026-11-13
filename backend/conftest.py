import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def logout_url():
    return reverse("accounts:logout")


@pytest.fixture
def register_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
    }


@pytest.fixture
def login_data():
    return {
        "username": "testuser",
        "password": "testpass123",
    }


@pytest.fixture
def short_link_data():
    return {
        "original_url": "https://example.com/example",
    }


@pytest.fixture
def short_link_with_title_data():
    return {
        "title": "Test title",
        "original_url": "https://example.com/example",
    }


@pytest.fixture
def registered_client(register_data):
    client = APIClient()
    url = reverse("accounts:register")
    response = client.post(url, register_data)
    response_data = response.json()
    refresh = client.cookies[settings.AUTH_REFRESH_COOKIE_NAME].value
    return client, response_data["access"], refresh


@pytest.fixture
def authenticated_client(registered_client):
    client, access_token, _ = registered_client
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client
