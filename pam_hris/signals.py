import json
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from pam_hris.models import SessionLog
from pathlib import Path

LOG_FILE = Path("C:\FinalYearProject\elk\logstash-pipeline\sessionlogs.json")  # must match logstash.conf

def append_log_to_file(data):
    with open(LOG_FILE, "a") as f:
        json.dump(data, f)
        f.write("\n")

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    session = SessionLog.objects.create(
        user=user,
        login_time=now(),
        ip_address=request.META.get('REMOTE_ADDR')
    )
    # write to file
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
            # update file with logout (append as new log)
            append_log_to_file({
                "id": session.id,
                "user_id": user.id,
                "login_time": str(session.login_time),
                "logout_time": str(session.logout_time),
                "ip_address": session.ip_address
            })
    except SessionLog.DoesNotExist:
        pass
