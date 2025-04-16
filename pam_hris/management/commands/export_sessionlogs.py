import json
from django.core.management.base import BaseCommand
from pam_hris.models import SessionLog

class Command(BaseCommand):
    help = 'Export session logs for Logstash (newline JSON format)'

    def handle(self, *args, **kwargs):
        logs = SessionLog.objects.all().values()
        with open('elk/logstash-pipeline/sessionlogs.json', 'w') as f:
            for entry in logs:
                json.dump(entry, f, default=str)
                f.write('\n')

        self.stdout.write(self.style.SUCCESS("✔ Exported session logs to sessionlogs.json (newline-delimited JSON)"))
