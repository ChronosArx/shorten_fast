import pytest
from pytest_mock import MockerFixture

from apps.links.services import (
    create_short_link,
    format_short_url,
    generate_qr,
    get_original_url,
)


@pytest.mark.django_db
def test_create_short_link() -> None:
    link = create_short_link(title="Test", original_url="https://example.com/example")

    assert link.title == "Test"
    assert link.original_url == "https://example.com/example"
    assert len(link.code) == 6
    assert link.short_url.endswith(link.code)
    assert link.clicks == 0
    assert link.user is None


@pytest.mark.django_db
def test_create_short_link_with_custom_length() -> None:
    link = create_short_link(
        title="Test",
        original_url="https://example.com/example",
        custom_length=10,
    )

    assert len(link.code) == 10


@pytest.mark.django_db
def test_create_short_link_generates_unique_code(mocker: MockerFixture) -> None:
    mocker.patch(
        "apps.links.services.generate_random_code",
        side_effect=["abc123", "abc123", "def456"],
    )

    first = create_short_link(title="First", original_url="https://example.com/1")
    second = create_short_link(title="Second", original_url="https://example.com/2")

    assert first.code == "abc123"
    assert second.code == "def456"


def test_format_short_url() -> None:
    assert format_short_url("abc123").endswith("/abc123")


@pytest.mark.django_db
def test_get_original_url() -> None:
    link = create_short_link(title="Test", original_url="https://example.com/example")

    assert get_original_url(link.code) == "https://example.com/example"

    link.refresh_from_db()
    assert link.clicks == 1


@pytest.mark.django_db
def test_get_original_url_increments_clicks() -> None:
    link = create_short_link(title="Test", original_url="https://example.com/example")

    get_original_url(link.code)
    get_original_url(link.code)

    link.refresh_from_db()
    assert link.clicks == 2


@pytest.mark.django_db
def test_get_original_url_unknown_code() -> None:
    assert get_original_url("noexiste") is None


def test_generate_qr() -> None:
    buffer = generate_qr("https://example.com")
    content = buffer.read()

    assert content.startswith(b"\x89PNG")
    assert len(content) > 0
