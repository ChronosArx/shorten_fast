from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.links.models import Link


@pytest.mark.django_db
def test_short_link(authenticated_client):
    url = reverse("shortlink-list")

    response = authenticated_client.post(
        url,
        data={
            "original_url": "https://example.com/example",
        },
    )
    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response_data
    assert "title" in response_data
    assert response_data["title"] is None
    assert "original_url" in response_data
    assert response_data["original_url"] == "https://example.com/example"
    assert "short_url" in response_data
    assert "code" in response_data
    assert response_data["code"].isalnum()
    assert len(response_data["code"]) == 6
    assert "expires_at" in response_data
    assert response_data["expires_at"] is None

    response = authenticated_client.post(
        url,
        data={
            "title": "Test title",
            "original_url": "https://example.com/example",
        },
    )
    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response_data
    assert "title" in response_data
    assert response_data["title"] == "Test title"
    assert "original_url" in response_data
    assert response_data["original_url"] == "https://example.com/example"
    assert "short_url" in response_data
    assert "code" in response_data
    assert response_data["code"].isalnum()
    assert len(response_data["code"]) == 6
    assert "expires_at" in response_data
    assert response_data["expires_at"] is None


@pytest.mark.django_db
def test_short_link_incorrect(authenticated_client):
    url = reverse("shortlink-list")
    response = authenticated_client.post(url, data={"original_url": "no-is-url"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_links(authenticated_client):
    url = reverse("shortlink-list")

    response_empty = authenticated_client.get(url)
    assert response_empty.status_code == status.HTTP_200_OK
    assert len(response_empty.json()) == 0

    authenticated_client.post(
        url,
        data={
            "title": "Link 1",
            "original_url": "https://example.com/1",
        },
    )
    authenticated_client.post(
        url,
        data={
            "title": "Link 2",
            "original_url": "https://example.com/2",
        },
    )

    response_items = authenticated_client.get(url)
    assert response_items.status_code == status.HTTP_200_OK
    assert len(response_items.json()) == 2


@pytest.mark.django_db
def test_get_links_incorrect(api_client):
    url = reverse("shortlink-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_link(authenticated_client):
    url_post = reverse("shortlink-list")
    response_post = authenticated_client.post(
        url_post,
        data={"title": "Test", "original_url": "https://example.com"},
    )
    short_link = response_post.json()
    link_id = short_link["id"]

    url_get = reverse("shortlink-detail", args=[link_id])
    response = authenticated_client.get(url_get)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "id" in response_data
    assert "title" in response_data
    assert response_data["title"] == "Test"
    assert "original_url" in response_data
    assert "short_url" in response_data
    assert "code" in response_data
    assert len(response_data["code"]) == 6
    assert "expires_at" in response_data
    assert response_data["expires_at"] is None


@pytest.mark.django_db
def test_get_link_incorrect(authenticated_client, api_client):
    url = reverse("shortlink-detail", args=[1])

    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_link(authenticated_client):
    url_post = reverse("shortlink-list")
    response = authenticated_client.post(
        url_post,
        data={"title": "Original", "original_url": "https://example.com"},
    )
    short_link = response.json()
    short_link["title"] = "Nuevo titulo"
    short_link["expires_at"] = (timezone.now() + timedelta(days=7)).isoformat()

    url_update = reverse("shortlink-detail", args=[short_link["id"]])
    response = authenticated_client.put(url_update, data=short_link)

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "id" in response_data
    assert "title" in response_data
    assert response_data["title"] is not None
    assert response_data["title"] == "Nuevo titulo"
    assert "original_url" in response_data
    assert "short_url" in response_data
    assert "code" in response_data
    assert len(response_data["code"]) == 6
    assert "expires_at" in response_data
    assert response_data["expires_at"] is not None


@pytest.mark.django_db
def test_update_link_with_past_expiration(authenticated_client):
    url_post = reverse("shortlink-list")
    response_post = authenticated_client.post(
        url_post,
        data={"title": "Test", "original_url": "https://example.com"},
    )
    link_id = response_post.json()["id"]

    url_update = reverse("shortlink-detail", args=[link_id])
    response = authenticated_client.put(
        url_update,
        data={
            "title": "Test",
            "original_url": "https://example.com",
            "expires_at": (timezone.now() - timedelta(days=1)).isoformat(),
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_link_incorrect(authenticated_client, api_client):
    url_update = reverse("shortlink-detail", args=[1])

    response = api_client.put(
        url_update,
        data={
            "title": "Test",
            "original_url": "https://example.com",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = authenticated_client.put(
        url_update,
        data={
            "title": "Test",
            "original_url": "https://example.com",
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url_post = reverse("shortlink-list")
    authenticated_client.post(
        url_post,
        data={
            "title": "Test",
            "original_url": "https://example.com",
        },
    )

    response = authenticated_client.put(url_update)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_link(authenticated_client):
    url_post = reverse("shortlink-list")
    response_post = authenticated_client.post(
        url_post,
        data={"title": "To Delete", "original_url": "https://example.com"},
    )
    link_id = response_post.json()["id"]

    url_delete = reverse("shortlink-detail", args=[link_id])
    response = authenticated_client.delete(url_delete)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_link_incorrect(authenticated_client, api_client):
    url = reverse("shortlink-detail", args=[1])

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_redirect(authenticated_client):
    url_post = reverse("shortlink-list")
    response_post = authenticated_client.post(
        url_post,
        data={"title": "Redirect Test", "original_url": "https://example.com"},
    )
    response_data = response_post.json()
    code = response_data["code"]

    url = reverse("redirects", args=[code])
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db
def test_redirect_incorrect(authenticated_client):
    url = reverse("redirects", args=["123456"])
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_link_with_expiration(authenticated_client):
    url = reverse("shortlink-list")
    expires_at = timezone.now() + timedelta(days=7)

    response = authenticated_client.post(
        url,
        data={
            "original_url": "https://example.com/example",
            "expires_at": expires_at.isoformat(),
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["expires_at"] is not None

    link = Link.objects.get(id=response_data["id"])
    assert link.expires_at is not None


@pytest.mark.django_db
def test_create_link_with_expiration_anonymous_ignored(api_client):
    url = reverse("shortlink-list")
    expires_at = timezone.now() + timedelta(days=7)

    response = api_client.post(
        url,
        data={
            "original_url": "https://example.com/example",
            "expires_at": expires_at.isoformat(),
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["expires_at"] is None


@pytest.mark.django_db
def test_create_link_with_past_expiration(authenticated_client):
    url = reverse("shortlink-list")
    expires_at = timezone.now() - timedelta(days=1)

    response = authenticated_client.post(
        url,
        data={
            "original_url": "https://example.com/example",
            "expires_at": expires_at.isoformat(),
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_qr(authenticated_client):
    url = reverse("shortlink-get-qr")

    response = authenticated_client.post(
        url,
        data={"original_url": "https://example.com"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Type"] == "image/png"


@pytest.mark.django_db
def test_get_qr_incorrect(api_client):
    url = reverse("shortlink-get-qr")

    response = api_client.post(
        url,
        data={"original_url": "no-is-url"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
