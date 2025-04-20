import json
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from .models import SessionLog
from pathlib import Path
from .models import User  


# Use raw string for Windows path to avoid escape issues
LOG_FILE = Path(r"C:/FinalYearProject/elk/logstash-pipeline/logs/sessionlogs.json")

def append_log_to_file(data):
    # Ensure JSON is dumped as one-liner (not pretty-printed)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(data, f)
        f.write("\n")

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    session = SessionLog.objects.create(
        user=user,
        login_time=now(),
        ip_address=request.META.get('REMOTE_ADDR')
    )
    append_log_to_file({
        "id": session.id,
        "user_id": user.id,
        "login_time": str(session.login_time),
        "logout_time": None,
        "ip_address": session.ip_address
    })

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    try:
        session = SessionLog.objects.filter(user=user).latest('login_time')
        if not session.logout_time:
            session.logout_time = now()
            session.save()
            append_log_to_file({
                "id": session.id,
                "user_id": user.id,
                "login_time": str(session.login_time),
                "logout_time": str(session.logout_time),
                "ip_address": session.ip_address
            })
    except SessionLog.DoesNotExist:
        pass
