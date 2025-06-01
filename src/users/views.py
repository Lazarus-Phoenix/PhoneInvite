# users/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import random
from django.utils import timezone
from datetime import timedelta

from src.users.models import User


class AuthView(APIView):
    def post(self, request):
        phone = request.data.get('phone')

        # Генерация OTP
        otp = str(random.randint(1000, 9999))
        expiry_time = timezone.now() + timedelta(seconds=random.randint(1, 2))

        # Поиск или создание пользователя
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            user = User.objects.create_user(
                phone=phone,
                username=f"user_{phone}"
            )

            # Генерация инвайт-кода для нового пользователя
            invite_code = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6))
            user.invite_code = invite_code
            user.save()

        # Обновление OTP
        user.otp = otp
        user.otp_expiry = expiry_time
        user.save()

        return Response({"status": "success"}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(phone=phone)

            # Проверка OTP и времени истечения
            if (user.otp == otp and
                    user.otp_expiry > timezone.now()):
                # Генерация токена доступа
                token = RefreshToken.for_user(user)

                return Response({
                    "token": str(token.access_token),
                    "invite_code": user.invite_code
                }, status=status.HTTP_200_OK)

            return Response(
                {"error": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Получение списка рефералов
        referrals = User.objects.filter(referrer=user)

        return Response({
            "phone": user.phone,
            "invite_code": user.invite_code,
            "used_invite_code": user.used_invite_code,
            "referrals_count": referrals.count(),
            "referrals": [
                {
                    "phone": ref.phone,
                    "joined_at": ref.date_joined
                } for ref in referrals
            ]
        })

    def post(self, request):
        invite_code = request.data.get('referrer_invite_code')

        try:
            referrer = User.objects.get(invite_code=invite_code)

            # Проверка что код не используется и существует
            if referrer != request.user and not request.user.used_invite_code:
                Referral.objects.create(
                    referrer=referrer,
                    referred=request.user
                )

                request.user.used_invite_code = invite_code
                request.user.save()

                return Response({"status": "success"})

            return Response(
                {"error": "Invalid invite code"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Invite code not found"},
                status=status.HTTP_404_NOT_FOUND
            )