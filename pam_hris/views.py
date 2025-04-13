from django.shortcuts import render
from django.http import HttpResponse
from .models import User, UserPriviledge, UserPriviledgeGroup
from django.contrib.auth.decorators import login_required

def home(request):
    return HttpResponse("Welcome to PAM-HRIS Home")

@login_required
def dashboard(request):
    user = request.user
    try:
        priv = UserPriviledge.objects.get(user=user)
        role = priv.priviledge_group.role_level

        if role == 1:
            return HttpResponse("Superuser Dashboard")
        elif role == 2:
            return HttpResponse("Privileged User Dashboard")
        else:
            return HttpResponse("Normal User Dashboard")
    except UserPriviledge.DoesNotExist:
        return HttpResponse("No privileges assigned to this user.")
