import string
import random
from shorten_fast.settings import DOMAIN_URL


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def genere_short_url(code: int):
    # Agregar mas logica TODO
    return f"{DOMAIN_URL}/{code}"
