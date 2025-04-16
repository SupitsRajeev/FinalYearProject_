from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now



class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    isHr = models.BooleanField(default=False)
    isIt = models.BooleanField(default=False)
    is_privileged = models.BooleanField(default=False)  # Add this for full PAM access
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class UserPriviledgeGroup(models.Model):
    name = models.CharField(max_length=120)
    role_level = models.IntegerField(unique=True)  # E.g., 1 = Normal, 2 = Manager, 3 = Admin
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Role Level {self.role_level})"


class UserPriviledge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priviledge_group = models.ForeignKey(UserPriviledgeGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} – {self.priviledge_group.name}"

    REQUIRED_FIELDS = ['email']            
    USERNAME_FIELD = 'username' 

from django.db import models
from django.utils.timezone import now
from .models import User  # or wherever your custom User model is

class SessionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=now)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


   