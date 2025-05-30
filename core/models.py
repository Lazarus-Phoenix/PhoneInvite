from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import random
import string


class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True)
    activated_invite = models.ForeignKey('self', on_delete=models.SET_NULL,
                                         null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_invite_code():
        characters = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choice(characters) for _ in range(6))
            if not User.objects.filter(invite_code=code).exists():
                return code

    def get_referrals(self):
        return User.objects.filter(activated_invite=self)