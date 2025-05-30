from django.urls import path
from .views import (
    AuthView,
    VerifyView,
    ProfileView,
    auth_page,
    profile_page
)

urlpatterns = [
    path('auth/', AuthView.as_view(), name='auth'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('auth-page/', auth_page, name='auth_page'),
    path('profile-page/', profile_page, name='profile_page'),
]