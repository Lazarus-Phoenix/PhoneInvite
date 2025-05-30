from django.urls import path
from .views import AuthView, VerifyView, ProfileView, auth_page, profile_page

urlpatterns = [
    path('api/auth/', AuthView.as_view(), name='auth'),
    path('api/verify/', VerifyView.as_view(), name='verify'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('auth/', auth_page, name='auth_page'),
    path('profile/', profile_page, name='profile_page'),
]
