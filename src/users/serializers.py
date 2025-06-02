from rest_framework import serializers
from .models import User, AuthCode
import time


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17)


class AuthCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17)
    code = serializers.CharField(max_length=4)


class UserProfileSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['phone', 'invite_code', 'activated_invite', 'referrals']
        read_only_fields = ['phone', 'invite_code', 'referrals']

    def get_referrals(self, obj):
        return list(obj.referrals.values_list('phone', flat=True))


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)
