from django.urls import reverse
from rest_framework.test import APITestCase
from .models import CustomUser


class AuthTestCase(APITestCase):
    def test_phone_auth(self):
        url = reverse('phone_auth')
        data = {'phone_number': '+79123456789'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        user = CustomUser.objects.get(phone_number=data['phone_number'])
        self.assertIsNotNone(user.auth_code)