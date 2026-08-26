import string
import io
import secrets

from django.conf import settings
from django.utils import timezone
from ua_parser import parse
import segno

from .models import Click, Link
from apps.users.models import User


def generate_random_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


def format_short_url(code: str) -> str:
    domain = settings.DOMAIN_URL.rstrip("/")
    return f"{domain}/{code}"


def create_short_link(
    title: str | None,
    original_url: str,
    user: User | None = None,
    custom_length: int = 6,
    expires_at=None,
) -> Link:
    while True:
        code = generate_random_code(length=custom_length)
        if not Link.objects.filter(code=code).exists():
            break

    full_url = format_short_url(code)

    link = Link.objects.create(
        title=title,
        original_url=original_url,
        short_url=full_url,
        code=code,
        user=user,
        expires_at=expires_at,
    )
    return link


def get_original_url_and_increment_click(
    code: str,
    referrer: str | None = None,
    user_agent: str | None = None,
    ip: str | None = None,
):
    link = Link.objects.filter(code=code).first()
    if not link:
        return None

    if link.expires_at and timezone.now() > link.expires_at:
        return None

    parsed_user_agent = parse(user_agent) if user_agent else None
    browser = (
        parsed_user_agent.user_agent.family
        if parsed_user_agent and parsed_user_agent.user_agent
        else None
    )
    device = (
        parsed_user_agent.device.family
        if parsed_user_agent and parsed_user_agent.device
        else None
    )
    Click.objects.create(
        link_id=link,
        timestamp=timezone.now().date(),
        ip=ip,
        referrer=referrer,
        browser=browser,
        device=device,
    )

    return link.original_url


def generate_qr(url: str):
    qr = segno.make_qr(url)
    buffer = io.BytesIO()
    qr.save(buffer, kind="png", scale=10, dark="black", light="white")
    buffer.seek(0)
    return buffer
