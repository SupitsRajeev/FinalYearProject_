from django.apps import AppConfig

class PamHrisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pam_hris'

    def ready(self):
        import pam_hris.signals  # only if you're using signals
