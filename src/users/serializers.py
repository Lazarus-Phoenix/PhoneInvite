from rest_framework import serializers
from phonenumbers import parse, is_valid_number
from .models import User
import time


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17)

    def validate_phone(self, value):
        try:
            parsed = parse(value, None)
            if not is_valid_number(parsed):
                raise serializers.ValidationError("Invalid phone number")
            return value
        except:
            raise serializers.ValidationError("Invalid phone number format")


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
        return list(obj.activated_referrals.values_list('phone', flat=True))


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)
