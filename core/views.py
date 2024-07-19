from django.shortcuts import redirect
import os
from django.conf import settings
from django.http import HttpResponse, Http404


def return_home_to_docs(request):
    return redirect("swagger-schema")

def download_logs(request):
    file_path = os.path.join(settings.BASE_DIR, 'general.log')
    print("file", file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="general.txt"'
            return response
    else:
        raise Http404("Log file not found")
