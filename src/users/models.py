from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, null=True, blank=True)
    used_invite_code = models.CharField(max_length=6, null=True, blank=True)
    otp = models.CharField(max_length=4, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrer_of')
    created_at = models.DateTimeField(auto_now_add=True)
