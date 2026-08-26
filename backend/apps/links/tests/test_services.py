from datetime import timedelta

import pytest
from django.utils import timezone

from apps.links.models import Click
from apps.links.services import (
    create_short_link,
    get_original_url_and_increment_click,
)


@pytest.mark.django_db
def test_get_original_url_creates_click():
    link = create_short_link(title="Test", original_url="https://example.com/example")
    chrome_ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )

    original_url = get_original_url_and_increment_click(
        code=link.code,
        referrer="https://google.com",
        user_agent=chrome_ua,
        ip="203.0.113.42",
    )

    assert original_url == "https://example.com/example"

    clicks = Click.objects.filter(link_id=link)
    assert clicks.count() == 1

    click = clicks.get()
    assert click.timestamp == timezone.now().date()
    assert click.ip == "203.0.113.42"
    assert click.referrer == "https://google.com"
    assert click.browser == "Chrome"
    assert click.device is None


@pytest.mark.django_db
def test_get_original_url_mobile_user_agent():
    link = create_short_link(title="Test", original_url="https://example.com/example")
    iphone_ua = (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
        "Mobile/15E148 Safari/604.1"
    )

    get_original_url_and_increment_click(code=link.code, user_agent=iphone_ua)

    click = Click.objects.get(link_id=link)
    assert click.browser == "Mobile Safari"
    assert click.device == "iPhone"


@pytest.mark.django_db
def test_get_original_url_without_user_agent():
    link = create_short_link(title="Test", original_url="https://example.com/example")

    get_original_url_and_increment_click(code=link.code)

    click = Click.objects.get(link_id=link)
    assert click.browser is None
    assert click.device is None


@pytest.mark.django_db
def test_get_original_url_unknown_code():
    result = get_original_url_and_increment_click(code="noexiste")

    assert result is None
    assert Click.objects.count() == 0


@pytest.mark.django_db
def test_get_original_url_increments_clicks():
    link = create_short_link(title="Test", original_url="https://example.com/example")

    for _ in range(2):
        get_original_url_and_increment_click(code=link.code)

    assert Click.objects.filter(link_id=link).count() == 2


@pytest.mark.django_db
def test_redirect_expired_link():
    link = create_short_link(
        title="Expired",
        original_url="https://example.com/example",
        expires_at=timezone.now() - timedelta(hours=1),
    )

    result = get_original_url_and_increment_click(code=link.code)

    assert result is None
    assert Click.objects.count() == 0


@pytest.mark.django_db
def test_redirect_not_expired_link():
    link = create_short_link(
        title="Valid",
        original_url="https://example.com/example",
        expires_at=timezone.now() + timedelta(days=1),
    )

    result = get_original_url_and_increment_click(code=link.code)

    assert result == "https://example.com/example"
    assert Click.objects.filter(link_id=link).count() == 1


@pytest.mark.django_db
def test_get_original_url_expiration_boundary(mocker):
    fixed_now = timezone.now()
    mocker.patch("apps.links.services.timezone.now", return_value=fixed_now)
    link = create_short_link(
        title="Boundary",
        original_url="https://example.com/example",
        expires_at=fixed_now,
    )

    result = get_original_url_and_increment_click(code=link.code)

    assert result == "https://example.com/example"
    assert Click.objects.filter(link_id=link).count() == 1
