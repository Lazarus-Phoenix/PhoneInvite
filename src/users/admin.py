from django.contrib import admin
from rest_framework.authtoken.admin import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "invite_code" ,)
    list_filter = ("phone", )
    search_fields = ("phone",)
