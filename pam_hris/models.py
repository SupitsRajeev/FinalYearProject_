from django.db import models

class User(models.Model):
    def __str__(self):
        return f"{self.name} ({self.email})"
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    isHr = models.BooleanField(default=False)
    isIt = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserPriviledgeGroup(models.Model):
    def __str__(self):
        return f"{self.name} ({self.email})"
    name = models.CharField(max_length=120)
    role_level = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserPriviledge(models.Model):
    def __str__(self):
        return f"{self.name} ({self.email})"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priviledge_group = models.ForeignKey(UserPriviledgeGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
