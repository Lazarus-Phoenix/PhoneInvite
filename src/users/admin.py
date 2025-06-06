from django.contrib import admin

from src.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "invite_code" ,)
    list_filter = ("phone", )
    search_fields = ("phone",)
