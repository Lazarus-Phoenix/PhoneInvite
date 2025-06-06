from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import secrets
import string


class User(AbstractUser):
    # Удаляем наследуемое поле username
    username = None

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'.",
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True)
    activated_invite = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activated_referrals",
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_invite_code():
        alphabet = string.ascii_uppercase + string.digits
        while True:
            code = "".join(secrets.choice(alphabet) for _ in range(6))
            if not User.objects.filter(invite_code=code).exists():
                return code

    def __str__(self):
        return self.phone


class AuthCode(models.Model):
    phone = models.CharField(max_length=17)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone}: {self.code}"


class Referral(models.Model):
    referrer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="referrals"
    )
    referred_user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="referral"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.phone} -> {self.referred_user.phone}"
