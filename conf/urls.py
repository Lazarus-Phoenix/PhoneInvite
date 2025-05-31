from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # Все API endpoints будут в /api/
    path('', include('core.urls')),     # Для веб-интерфейса
]