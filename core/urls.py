from django.urls import path
from .views import AuthView, VerifyView, ProfileView, ReferralsView

urlpatterns = [
    path('auth/', AuthView.as_view(), name='auth'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('referrals/', ReferralsView.as_view(), name='referrals'),
]
