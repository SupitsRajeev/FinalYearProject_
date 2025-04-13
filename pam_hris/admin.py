from django.contrib import admin
from .models import User, UserPriviledgeGroup, UserPriviledge

admin.site.register(User)
admin.site.register(UserPriviledgeGroup)
admin.site.register(UserPriviledge)
