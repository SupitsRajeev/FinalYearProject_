# Generated by Django 4.2.9 on 2025-04-19 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_management', '0004_delete_manageduser_alter_sessionlog_login_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionlog',
            name='activity',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
