from rest_framework import serializers
from .models import CustomUser


class UserProfileSerializer(serializers.ModelSerializer):
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'invite_code', 'activated_invite', 'referred_users']

    def get_referred_users(self, obj):
        return list(CustomUser.objects.filter(activated_invite=obj.invite_code).values_list('phone_number', flat=True))