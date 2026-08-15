import string
import io
import secrets

from django.conf import settings
from django.db.models import F
import segno

from .models import Link
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
) -> Link:
    while True:
        code = generate_random_code(length=custom_length)
        if not Link.objects.filter(code=code).exists():
            break

    full_url = format_short_url(code)

    link = Link.objects.create(
        title=title, original_url=original_url, short_url=full_url, code=code, user=user
    )
    return link


def get_original_url_and_increment_click(code):
    link = Link.objects.filter(code=code).first()
    if not link:
        return None
    original_url = link.original_url
    link.clicks = F("clicks") + 1
    link.save(update_fields=["clicks"])

    return original_url


def generate_qr(url: str):
    qr = segno.make_qr(url)
    buffer = io.BytesIO()
    qr.save(buffer, kind="png", scale=10, dark="black", light="white")
    buffer.seek(0)
    return buffer
