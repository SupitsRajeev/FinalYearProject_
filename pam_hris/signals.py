from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from pam_hris.models import SessionLog


# ✅ Only use one consistent model
from it_management.models import SessionLog  # or from pam_hris.models if that’s where you store logs

# ✅ LOGIN
@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    SessionLog.objects.create(
        user=user,
        login_time=now(),
        ip_address=request.META.get('REMOTE_ADDR')
    )

# ✅ LOGOUT
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    try:
        last_session = SessionLog.objects.filter(user=user).latest('login_time')
        if not last_session.logout_time:
            last_session.logout_time = now()
            last_session.save()
            print("✅ Logout time updated!")
    except SessionLog.DoesNotExist:
        print("⚠️ No session found to update logout time.")
