from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('phone', 'invite_code', 'activated_invite', 'date_joined')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('phone', 'invite_code')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('invite_code', 'activated_invite')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )


admin.site.register(User, CustomUserAdmin)