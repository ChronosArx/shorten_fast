from django.db import models
from django.conf import settings


class ShortLink(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    original_url = models.URLField()
    short_url = models.URLField()
    code = models.CharField(max_length=6, unique=True)
    clicks = models.IntegerField(default=0)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
