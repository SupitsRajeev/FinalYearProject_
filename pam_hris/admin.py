from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserPriviledge, UserPriviledgeGroup, SessionLog

@admin.register(SessionLog)
class SessionLogAdmin(admin.ModelAdmin):
    list_display = ("user", "login_time", "logout_time", "ip_address")
    list_filter = ("user", "ip_address")
    search_fields = ("user__username", "ip_address")
    ordering = ("-login_time",)

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'isHr', 'isIt', 'is_privileged', 'is_active', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles', {
            'fields': ('isHr', 'isIt', 'is_privileged'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserPriviledge)
admin.site.register(UserPriviledgeGroup)
# admin.site.uregister(SessionLog)
