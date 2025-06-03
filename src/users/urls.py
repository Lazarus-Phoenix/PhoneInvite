from django.urls import path
from .views import PhoneAuthView, VerifyView, ProfileView

urlpatterns = [
    path('auth/phone/', PhoneAuthView.as_view(), name='auth'),
    path('auth/verify/', VerifyView.as_view(), name='verify'),
    path('profile/', ProfileView.as_view(), name='profile'),
]