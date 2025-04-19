from django.db import models
from django.utils.timezone import now
from pam_hris.models import User  # or your custom User model path

class SessionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_logs')
    login_time = models.DateTimeField(default=now)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    activity = models.CharField(max_length=255, null=True, blank=True)  # ✅ New field

    def __str__(self):
        return f"{self.user.username} - {self.login_time} - {self.activity}"

