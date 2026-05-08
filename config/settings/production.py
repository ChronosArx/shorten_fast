from .base import *
from .base import env
from datetime import timedelta

DEBUG = False
SECRET_KEY = env("SECRET_KEY")
EXPIRE_TIME_TOKEN_MINUTES = env.int("EXPIRE_TIME_TOKEN_MINUTES")
EXPIRE_TIME_TOKEN_DAYS = env.int("EXPIRE_TIME_TOKEN_DAYS")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
DATABASES = {"default": env.db()}


THIRD_MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=EXPIRE_TIME_TOKEN_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=EXPIRE_TIME_TOKEN_DAYS),
}
