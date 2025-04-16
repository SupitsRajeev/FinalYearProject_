from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserPriviledge, User, SessionLog
from hr_management.models import HREmployee, HRSalarySheet
#from it_management.models import ManagedUser
from django.contrib.auth import logout


# 🌐 Landing Page
def landing_page(request):
    return render(request, 'landing.html')


# 🔐 Post-login Role-Based Redirection
@login_required
def login_redirect(request):
    user = request.user

    if user.is_superuser:
        return redirect('hr_application')  # or a separate admin dashboard if needed

    try:
        priv = UserPriviledge.objects.get(user=user)
        role = priv.priviledge_group.role_level

        if role == 1:
            return redirect('hr_dashboard')
        elif role == 2:
            return redirect('it_dashboard')
        elif role == 3:
            return redirect('hr_application')  # Admin with role 3
        else:
            return redirect('no_privilege')
    except UserPriviledge.DoesNotExist:
        return redirect('no_privilege')



# 🧠 Unified Dashboard (used by Admin, accessible to all)
@login_required
def hr_application_view(request):
    user = request.user

    # ✅ Allow superuser without checking UserPriviledge
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
        'it_users': None,  # You removed ManagedUser model, right?
        'it_sessions': SessionLog.objects.all() if role in [2, 3] else None,
    }

    return render(request, 'partials/hr_application.html', context)



# 📂 HR-Only Dashboard
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


# 🖥️ IT-Only Dashboard
@login_required
def it_dashboard_view(request):
    if not request.user.isIt and not request.user.is_privileged:
        return redirect('no_privilege')

    SessionLog.objects.create(user=request.user, activity="Accessed IT Dashboard")

    context = {
        'it_users': ManagedUser.objects.all(),
        'it_sessions': SessionLog.objects.all(),
    }
    return render

@login_required
def no_privilege_fallback(request):
    return render(request, 'dashboards/no_privilege.html')

def logout_view(request):
    logout(request)
    return redirect('login')
