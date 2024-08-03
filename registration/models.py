from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class ActivationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=32)
    date = models.DateTimeField(default=timezone.now, editable=False)

    def is_expired(self):
        expiration_time = self.date + timedelta(hours=24)
        return timezone.now() > expiration_time

    def __str__(self):
        return self.code
