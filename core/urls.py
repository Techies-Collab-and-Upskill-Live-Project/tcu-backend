from django.urls import path
from .views import download_logs

urlpatterns = [
    path('download-logs/', download_logs, name='download_logs'),
]
