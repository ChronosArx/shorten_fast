import pytest
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def api_client():
    return APIClient()


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
    url = reverse("register")
    response = client.post(url, register_data)
    response_data = response.json()
    return client, response_data.get("access"), response_data.get("refresh")


@pytest.fixture
def authenticated_client(registered_client):
    client, access_token, _ = registered_client
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client
