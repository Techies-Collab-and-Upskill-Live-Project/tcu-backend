import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from internship.models import InternshipApplication
from internship.serializers import InternshipApplicationSerializer
from .utils import SlackBot

slack_bot = SlackBot()

@method_decorator(csrf_exempt, name='dispatch')
class SlackEventsView(View):

    def post(self, request, *args, **kwargs):
        try:
            form_data = request.POST

            if 'command' in form_data and form_data['command'] == '/getapplicants':
                user_id = form_data['user_id']
                response_data = self.handle_get_applications()
                text = self.format_applications(response_data)
                slack_bot.send_message_to_user(user_id, text)
                return JsonResponse({'status': 'ok'})

            # Handling URL verification challenge
            body = json.loads(request.body.decode('utf-8'))
            if body and 'type' in body and body['type'] == 'url_verification':
                return JsonResponse({'challenge': body['challenge']})
        
        except Exception as e:
            print("e", e)
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'error': 'Unsupported Media Type'}, status=415)

    def handle_get_applications(self):
        try:
            applications = InternshipApplication.objects.all()
            serializer = InternshipApplicationSerializer(applications, many=True)
            return {"total_applications": applications.count(), "applications": serializer.data}
        except Exception as e:
            return f"Error: {str(e)}"

    def format_applications(self, data):
        if isinstance(data, str):
            return [], data  # Return an empty list and the error message if it's a string

        # applications = data.get('applications', [])
        # blocks = []
        text = f"Good day boss. \nWe have {data['total_applications']} total applications currently\n\nKindly get them here: https://www.tculive.com/user\n\nThanks, \nTCU dev team"
        

        return text
