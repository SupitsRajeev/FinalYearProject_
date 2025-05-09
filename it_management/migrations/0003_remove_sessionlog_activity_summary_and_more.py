# Generated by Django 4.2.9 on 2025-04-16 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('it_management', '0002_manageduser_sessionlog_delete_itasset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessionlog',
            name='activity_summary',
        ),
        migrations.AlterField(
            model_name='sessionlog',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sessionlog',
            name='login_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sessionlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='it_session_logs', to=settings.AUTH_USER_MODEL),
        ),
    ]
