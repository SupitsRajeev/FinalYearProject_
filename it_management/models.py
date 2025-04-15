from django.db import models
from pam_hris.models import User  # use your custom user model

class SessionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)
    activity_summary = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


class ManagedUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} - {self.role}"
