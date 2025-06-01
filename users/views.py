from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time
from .models import CustomUser
import random
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .serializers import UserProfileSerializer

class PhoneAuthView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Генерация 4-значного кода
        auth_code = str(random.randint(1000, 9999))

        # Имитация задержки отправки SMS
        time.sleep(2)

        # Сохранение или обновление пользователя
        user, created = CustomUser.objects.get_or_create(
            phone_number=phone_number,
            defaults={'username': phone_number}
        )
        user.auth_code = auth_code
        user.save()

        return Response({'message': 'Auth code sent'})


class VerifyCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        auth_code = request.data.get('auth_code')

        try:
            user = CustomUser.objects.get(phone_number=phone_number, auth_code=auth_code)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid code or phone number'}, status=status.HTTP_400_BAD_REQUEST)

        # Здесь можно добавить логику для JWT токена, если нужно
        return Response({
            'message': 'Successfully authenticated',
            'invite_code': user.invite_code
        })





class UserProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class ActivateInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        invite_code = request.data.get('invite_code')

        if not invite_code:
            return Response({'error': 'Invite code is required'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.activated_invite:
            return Response({'error': 'You already activated an invite code'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            inviting_user = CustomUser.objects.get(invite_code=invite_code)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid invite code'}, status=status.HTTP_400_BAD_REQUEST)

        if inviting_user == request.user:
            return Response({'error': 'You cannot use your own invite code'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.activated_invite = invite_code
        request.user.save()

        return Response({'message': 'Invite code activated successfully'})