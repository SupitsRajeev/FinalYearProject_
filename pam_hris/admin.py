from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserPriviledge, UserPriviledgeGroup
from it_management.models import SessionLog



class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'isHr', 'is_privileged', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles', {
            'fields': ('isHr', 'isIt', 'is_privileged'),
        }),
    )



admin.site.register(User, CustomUserAdmin)
admin.site.register(UserPriviledge)
admin.site.register(UserPriviledgeGroup)
admin.site.register(SessionLog)
