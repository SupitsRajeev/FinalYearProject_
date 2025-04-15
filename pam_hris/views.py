from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserPriviledge, User
from hr_management.models import HREmployee, HRSalarySheet
from it_management.models import ManagedUser, SessionLog  # Assuming you renamed these




def landing_page(request):
    return render(request, 'landing.html')


@login_required
def login_redirect(request):
    user = request.user
    try:
        priv = UserPriviledge.objects.get(user=user)
        role = priv.priviledge_group.role_level

        if role == 1:
            return redirect('hr_dashboard')  # e.g., /hr/dashboard/
        elif role == 2:
            return redirect('it_dashboard')  # e.g., /it/dashboard/
        elif role == 3:
            return redirect('admin_dashboard')  # or just choose one
        else:
            return redirect('no_privilege')
    except UserPriviledge.DoesNotExist:
        return redirect('no_privilege')

@login_required
def hr_application_view(request):
   return render(request, 'partials/hr_application.html')


@login_required
def dashboard(request):
    user = request.user

    try:
        priv = UserPriviledge.objects.get(user=user)
        role = priv.priviledge_group.role_level

        context = {
            'role': role,
            'hr_employees': None,
            'hr_salaries': None,
            'it_users': None,
            'it_sessions': None,
        }

        # HR + Admin
        if role == 1 or role == 3:
            context['hr_employees'] = HREmployee.objects.all()
            context['hr_salaries'] = HRSalarySheet.objects.all()

        # IT + Admin
        if role == 2 or role == 3:
            context['it_users'] = ManagedUser.objects.all()
            context['it_sessions'] = SessionLog.objects.all()

        return render(request, 'partials/hr_application.html', context)

    except UserPriviledge.DoesNotExist:
        return render(request, 'dashboards/no_privilege.html')
    
@login_required
def hr_dashboard(request):
    return dashboard(request)

@login_required
def it_dashboard(request):
    return dashboard(request)

@login_required
def admin_dashboard(request):
    return dashboard(request)

    
