from django.db import models
from django.conf import settings


class Link(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    original_url = models.URLField()
    short_url = models.URLField()
    code = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )


class Click(models.Model):
    link_id = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="clicks")
    timestamp = models.DateField()
    ip = models.GenericIPAddressField(null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    device = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
