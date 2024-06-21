# apps.py
from django.apps import AppConfig

class InternshipAppConfig(AppConfig):
    name = 'internship'

    def ready(self):
        import internship.signals
