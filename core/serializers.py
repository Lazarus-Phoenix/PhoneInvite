from rest_framework import serializers
from .models import User


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17)


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17)
    code = serializers.CharField(max_length=4)


class UserProfileSerializer(serializers.ModelSerializer):
    activated_invite = serializers.CharField(source='activated_invite.invite_code', read_only=True)

    class Meta:
        model = User
        fields = ['phone', 'invite_code', 'activated_invite']


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'date_joined']