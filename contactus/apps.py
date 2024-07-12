# apps.py
from django.apps import AppConfig

class ContactUsAppConfig(AppConfig):
    name = 'contactus'

    def ready(self):
        import contactus.signals
