from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserPriviledge, User, SessionLog
from hr_management.models import HREmployee, HRSalarySheet
# from it_management.models import ManagedUser
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST



def landing_page(request):
    return render(request, 'landing.html')


@login_required
def login_redirect(request):
    user = request.user

    if user.is_superuser:
        return render(request, 'partials/base_dashboard.html', {
            'user': user,
            'hr_employees': HREmployee.objects.all(),
            'hr_salaries': HRSalarySheet.objects.all(),
            'it_sessions': SessionLog.objects.all(),
        })

    try:
        priv = UserPriviledge.objects.get(user=user)
        role = priv.priviledge_group.role_level

        if role == 1:
            return redirect('hr_dashboard')
        elif role == 2:
            return redirect('it_dashboard')
        elif role == 3:
            return redirect('hr_application')  # Optional: adjust if not needed anymore
        else:
            return redirect('no_privilege')
    except UserPriviledge.DoesNotExist:
        return redirect('no_privilege')



@login_required
def hr_application_view(request):
    user = request.user

    if user.is_superuser:
        role = 3
    else:
        try:
            priv = UserPriviledge.objects.get(user=user)
            role = priv.priviledge_group.role_level
        except UserPriviledge.DoesNotExist:
            return redirect('no_privilege')

    context = {
        'role': role,
        'hr_employees': HREmployee.objects.all() if role in [1, 3] else None,
        'hr_salaries': HRSalarySheet.objects.all() if role in [1, 3] else None,
        'it_users': None,
        'it_sessions': SessionLog.objects.all() if role in [2, 3] else None,
    }

    return render(request, 'partials/base_dashboard.html', context)


@login_required
def hr_dashboard_view(request):
    if not request.user.isHr and not request.user.is_privileged:
        return redirect('no_privilege')

    SessionLog.objects.create(user=request.user, activity="Accessed HR Dashboard")

    context = {
        'hr_employees': HREmployee.objects.all(),
        'hr_salaries': HRSalarySheet.objects.all(),
    }
    return render(request, 'dashboards/hr_dashboard.html', context)


@login_required
def it_dashboard_view(request):
    if not request.user.isIt and not request.user.is_privileged:
        return redirect('no_privilege')

    SessionLog.objects.create(user=request.user, activity="Accessed IT Dashboard")

    context = {
        'it_users': None,  # ← Placeholder, since ManagedUser is commented
        'it_sessions': SessionLog.objects.all(),
    }
    return render(request, 'dashboards/it_dashboard.html', context)  # ✅ Fixed render


@login_required
def no_privilege_fallback(request):
    return render(request, 'dashboards/no_privilege.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_users_view(request):
    users = User.objects.exclude(is_superuser=True)  # You can change this if needed
    return render(request, 'partials/user_management.html', {'users': users})



@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def toggle_user_status(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        if user.is_superuser:
            return HttpResponseForbidden("Cannot deactivate superuser.")
        user.is_active = not user.is_active
        user.save()
    except User.DoesNotExist:
        pass
    return redirect('manage_users')
