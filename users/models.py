from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string


def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, default=generate_invite_code, unique=True)
    activated_invite = models.CharField(max_length=6, blank=True, null=True)
    auth_code = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return self.phone_number
