from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import (
    PhoneSerializer,
    VerifyCodeSerializer,
    UserProfileSerializer,
    InviteCodeSerializer,
    ReferralSerializer
)
from .services import send_verification_code, verify_code
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AuthView(APIView):
    @swagger_auto_schema(request_body=PhoneSerializer)
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            send_verification_code(phone)
            return Response({'status': 'verification code sent'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(APIView):
    @swagger_auto_schema(request_body=VerifyCodeSerializer)
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']

            if verify_code(phone, code):
                user, created = User.objects.get_or_create(phone=phone)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': 'success',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserProfileSerializer})
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=InviteCodeSerializer)
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


class ReferralsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ReferralSerializer(many=True)})
    def get(self, request):
        referrals = request.user.get_referrals()
        serializer = ReferralSerializer(referrals, many=True)
        return Response(serializer.data)