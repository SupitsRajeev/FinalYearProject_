from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserPriviledge

@login_required
def dashboard(request):
    user = request.user
    try:
        priv = UserPriviledge.objects.get(user=user)
        role = priv.priviledge_group.role_level
        is_hr = user.isHr
        is_it = user.isIt

        return render(request, 'dashboards/main_dashboard.html', {
            'role': role,
            'is_hr': is_hr,
            'is_it': is_it,
        })
    except UserPriviledge.DoesNotExist:
        return render(request, 'dashboards/no_privilege.html')
