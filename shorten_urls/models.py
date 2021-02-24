from django.db import models
from .env import DOMAIN


class URL(models.Model):
    long_url = models.URLField(max_length=300)
    short_url = models.URLField(max_length=100)
    scheme = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.scheme}://{self.long_url} --> {DOMAIN}/{self.short_url}'
