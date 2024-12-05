from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ShortLink(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    original_url = models.URLField()
    short_url = models.URLField()
    code = models.CharField(max_length=6, unique=True)
    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
