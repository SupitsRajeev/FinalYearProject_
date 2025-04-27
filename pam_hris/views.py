from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import UserPriviledge, User, SessionLog, PrivilegeRequest
from hr_management.models import HREmployee, HRSalarySheet
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path


# ----------------------------
# Public & Authentication Views
# ----------------------------

def landing_page(request):
    return render(request, 'landing.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ----------------------------
# Role-Based Redirect Handler
# ----------------------------

@login_required
def login_redirect(request):
    user = request.user

    # Superuser → Admin Dashboard
    if user.is_superuser:
        pending_requests = PrivilegeRequest.objects.filter(is_reviewed=False)
        return render(request, 'partials/base_dashboard.html', {
            'user': user,
            'hr_employees': HREmployee.objects.all(),
            'hr_salaries': HRSalarySheet.objects.all(),
            'it_sessions': SessionLog.objects.all(),
            'pending_requests': pending_requests,
        })

    # HR → HR dashboard
    if user.isHr:
        return redirect('hr_dashboard')

    # IT → IT dashboard
    if user.isIt:
        return redirect('it_dashboard')

    # Privileged access → HR Application
    if user.is_privileged:
        return redirect('hr_application')

    # Fallback → No Privilege
    return redirect('no_privilege')


# ----------------------------
# Dashboard Views
# ----------------------------

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
        'it_users': None,
        'it_sessions': SessionLog.objects.all(),
    }
    return render(request, 'dashboards/it_dashboard.html', context)


@login_required
def no_privilege_fallback(request):
    return render(request, 'dashboards/no_privilege.html')


# ----------------------------
# Admin User Management Views
# ----------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_users_view(request):
    users = User.objects.exclude(is_superuser=True)
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


# ----------------------------
# Privileged Access Request Views
# ----------------------------

# IT users can request elevated (privileged) access
@login_required
@user_passes_test(lambda u: u.isIt and not u.is_privileged)
def request_privilege_view(request):
    existing = PrivilegeRequest.objects.filter(user=request.user, is_reviewed=False).first()

    if existing:
        return render(request, 'partials/request_status.html', {"message": "You already have a pending request."})

    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        PrivilegeRequest.objects.create(user=request.user, reason=reason)
        return render(request, 'partials/request_status.html', {"message": "Request submitted successfully."})

    return render(request, 'partials/request_form.html')


# Superuser can view all unreviewed privilege requests
@login_required
@user_passes_test(lambda u: u.is_superuser)
def review_privilege_requests_view(request):
    requests = PrivilegeRequest.objects.filter(is_reviewed=False)
    return render(request, 'partials/request_status.html', {"requests": requests})


# Superuser approves a specific request and grants privileged access
@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def approve_privilege_view(request, request_id):
    try:
        req = PrivilegeRequest.objects.get(id=request_id)
        req.is_reviewed = True
        req.is_approved = True
        req.save()

        user = req.user
        user.is_privileged = True
        user.save()
    except PrivilegeRequest.DoesNotExist:
        pass

    return redirect('review_privilege_requests')


# Superuser can revoke previously granted privileged access
@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def revoke_privilege_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        if user.is_privileged:
            user.is_privileged = False
            user.save()
    except User.DoesNotExist:
        pass
    return redirect('manage_users')

# -------------For rendering session logs in dashboard---------------
@login_required
def session_logs_view(request):
    logs = SessionLog.objects.all().order_by('-login_time')  # Latest first
    return render(request, 'partials/session_logs.html', {'logs': logs})


@login_required
def download_session_logs_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="session_logs.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Session Monitoring Report")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 100, "Username")
    p.drawString(200, height - 100, "Login Time")
    p.drawString(350, height - 100, "Logout Time")
    p.drawString(500, height - 100, "IP Address")

    logs = SessionLog.objects.all().order_by('-login_time')
    y = height - 120
    p.setFont("Helvetica", 10)
    
    for log in logs:
        p.drawString(50, y, log.user.username)
        p.drawString(200, y, log.login_time.strftime('%Y-%m-%d %H:%M:%S'))
        p.drawString(350, y, log.logout_time.strftime('%Y-%m-%d %H:%M:%S') if log.logout_time else 'Still Active')
        p.drawString(500, y, log.ip_address or 'N/A')
        y -= 20

        if y < 50:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 10)

    p.showPage()
    p.save()

    # Add this part to LOG the Download Event
    SessionLog.objects.create(
        user=request.user,
        activity="Downloaded Session Logs"
    )
    # Save to Server Folder also
    folder_path = Path(r"C:/FinalYearProject/elk/logstash-pipeline/logs/")
    folder_path.mkdir(parents=True, exist_ok=True)
    with open(folder_path / 'sessionlogs.pdf', 'wb') as f:
     f.write(response.content)

    return response