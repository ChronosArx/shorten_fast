import string
import io
import secrets

from django.conf import settings
import segno

from .models import ShortLink


def generate_random_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


def format_short_url(code: str) -> str:
    domain = settings.DOMAIN_URL.rstrip("/")
    return f"{domain}/{code}"


def create_short_link_service(custom_length: int = 6):
    while True:
        code = generate_random_code(length=custom_length)
        if not ShortLink.objects.filter(code=code).exists():
            break

    full_url = format_short_url(code)
    return full_url, code


def generate_qr(url: str):
    qr = segno.make_qr(url)
    buffer = io.BytesIO()
    qr.save(buffer, kind="png", scale=10, dark="black", light="white")
    buffer.seek(0)
    return buffer
