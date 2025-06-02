from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User, AuthCode
from .serializers import (
    PhoneSerializer,
    AuthCodeSerializer,
    UserProfileSerializer,
    InviteCodeSerializer
)
import random
import time
from django.shortcuts import get_object_or_404

from rest_framework.throttling import AnonRateThrottle

class AuthPhoneThrottle(AnonRateThrottle):
    '''
     устанавливает лимит в 3 запроса в час c одного IP
    '''
    rate = '3/hour'

class AuthPhoneView(APIView): # определяется представление для обработки запросов
    throttle_classes = [AuthPhoneThrottle] # подключается созданный throttle к этому view


class AuthView(APIView):
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']

            # Имитация отправки кода
            code = str(random.randint(1000, 9999))
            AuthCode.objects.create(phone=phone, code=code)

            # Задержка для имитации отправки SMS
            time.sleep(2)

            return Response(
                {'detail': 'Auth code sent'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(APIView):
    def post(self, request):
        serializer = AuthCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']

            auth_code = AuthCode.objects.filter(
                phone=phone,
                code=code
            ).order_by('-created_at').first()

            if auth_code:
                user, created = User.objects.get_or_create(phone=phone)
                return Response(
                    {'token': user.auth_token.key},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'detail': 'Invalid code'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        serializer = InviteCodeSerializer(data=request.data)
        if serializer.is_valid():
            invite_code = serializer.validated_data['invite_code']

            if request.user.activated_invite:
                return Response(
                    {'detail': 'You already activated an invite code'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                referrer = User.objects.get(invite_code=invite_code)
                if referrer == request.user:
                    return Response(
                        {'detail': 'You cannot use your own invite code'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                request.user.activated_invite = referrer
                request.user.save()
                return Response(
                    {'detail': 'Invite code activated successfully'},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {'detail': 'Invalid invite code'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)