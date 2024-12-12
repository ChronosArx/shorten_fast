from .base import *
from datetime import timedelta

DEBUG = True
SECRET_KEY = env("SECRET_KEY")
EXPIRE_TIME_TOKEN_MINUTES = env.int("EXPIRE_TIME_TOKEN_MINUTES", default=5)
EXPIRE_TIME_TOKEN_DAYS = env.int("EXPIRE_TIME_TOKEN_DAYS", default=7)
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
DATABASES = {"default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3")}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=EXPIRE_TIME_TOKEN_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=EXPIRE_TIME_TOKEN_DAYS),
}
