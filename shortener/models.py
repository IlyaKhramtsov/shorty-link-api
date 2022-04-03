from django.contrib.auth.models import User
from django.db import models

from .utils import create_short_id


class Shortener(models.Model):
    link = models.URLField()
    short_id = models.SlugField(max_length=10, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.link} to {self.short_id}'

    def save(self, *args, **kwargs):
        if not self.short_id:
            self.short_id = create_short_id(self)
        super().save(*args, **kwargs)
