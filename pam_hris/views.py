from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserPriviledge, User
from hr_management.models import HREmployee
from it_management.models import ITAsset



def landing_page(request):
    return render(request, 'landing.html')


@login_required
def hr_application_view(request):
    return render(request, 'hr_application.html')


@login_required
def dashboard(request):
    user = request.user

    try:
        # Using your custom User model directly
        priv = UserPriviledge.objects.get(user=user)
        role = priv.priviledge_group.role_level

        context = {
            'role': role,
            'is_hr': user.isHr,
            'is_it': user.isIt,
            'is_privileged': user.is_privileged,
            'hr_data': None,
            'it_data': None
        }

        # Load HR data if user has HR access
        if user.isHr or user.is_privileged:
            context['hr_data'] = HRModel.objects.all()

        # Load IT data if user has IT access
        if user.isIt or user.is_privileged:
            context['it_data'] = ITModel.objects.all()

        return render(request, 'hr_application.html', context)

    except UserPriviledge.DoesNotExist:
        return render(request, 'dashboards/no_privilege.html')
