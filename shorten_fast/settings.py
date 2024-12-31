import os

ENVIRONMENT = os.getenv("DJANGO_ENV", "development")

if ENVIRONMENT == "production":
    from .config.production import *
elif ENVIRONMENT == "development":
    from .config.dev import *
else:
    raise ValueError(f"Unknown environment: {ENVIRONMENT}")
