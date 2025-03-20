from django.shortcuts import redirect
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

def return_home_to_docs(request):
    return redirect("swagger-schema")

@login_required
def download_logs(request):
    file_path = os.path.join(settings.BASE_DIR, 'general.log')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="general.txt"'
            return response
    else:
        raise Http404("Log file not found")
