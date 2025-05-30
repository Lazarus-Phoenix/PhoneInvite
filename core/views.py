from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .services import send_verification_code, verify_code
from .serializers import (
    PhoneSerializer,
    VerifyCodeSerializer,
    UserProfileSerializer,
    InviteCodeSerializer
)
from .models import User
from django.contrib.auth import login
from django.shortcuts import render


class AuthView(APIView):
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            send_verification_code(phone)
            return Response({'status': 'verification code sent'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']

            if verify_code(phone, code):
                user, created = User.objects.get_or_create(phone=phone)
                login(request, user)
                return Response({'status': 'success'})
            return Response({'error': 'invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if user.activated_invite:
            return Response(
                {'error': 'You already activated an invite code'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = InviteCodeSerializer(data=request.data)
        if serializer.is_valid():
            invite_code = serializer.validated_data['invite_code']
            try:
                inviter = User.objects.get(invite_code=invite_code)
                if inviter == user:
                    return Response(
                        {'error': 'You cannot use your own invite code'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                user.activated_invite = inviter
                user.save()
                return Response({'status': 'invite code activated'})
            except User.DoesNotExist:
                return Response(
                    {'error': 'invalid invite code'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def auth_page(request):
    return render(request, 'core/auth.html')


def profile_page(request):
    return render(request, 'core/profile.html')
