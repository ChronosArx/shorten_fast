import string
import random


def generate_code(length=6):
    characters = string.digits
    return "".join(random.choice(characters) for _ in range(length))
