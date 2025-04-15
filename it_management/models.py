from django.db import models

class ITAsset(models.Model):
    device = models.CharField(max_length=100)
    assigned_to = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device} - {self.status}"
