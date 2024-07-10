import os
import json
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.response import Response
from rest_framework import status

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
                response_blocks, text = self.format_applications(response_data)
                slack_bot.send_message_to_user(user_id, text, response_blocks)
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

        applications = data.get('applications', [])
        # blocks = []
        text = f"Total Applications: {data['total_applications']}\n\n"
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Total Applications:* {data['total_applications']}"
                }
            }
        ]

        for app in applications:
            text += (
                f"Full Name: {app['full_name']}\n"
                f"Email: {app['email']}\n"
                f"Skill: {app['skill']} ({app['experience']})\n"
                f"About Skill: {app['about_skill']}\n"
                f"Twitter: {app['twitter_handle']}\n"
                f"LinkedIn: {app['linkedin']}\n"
                f"Commitment: {'Yes' if app['commitment'] else 'No'}\n"
                f"Birthdate: {app['birthdate']}\n\n"
            )
            blocks.append({"type": "divider"})
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*Full Name:* {app['full_name']}\n"
                        f"*Email:* {app['email']}\n"
                        f"*Skill:* {app['skill']} ({app['experience']})\n"
                        f"*About Skill:* {app['about_skill']}\n"
                        f"*Twitter:* {app['twitter_handle']}\n"
                        f"*LinkedIn:* {app['linkedin']}\n"
                        f"*Commitment:* {'Yes' if app['commitment'] else 'No'}\n"
                        f"*Birthdate:* {app['birthdate']}"
                    )
                }
            })
        return {"blocks": blocks, "type": "home"}, text

    # def send_message(self, user_id, blocks, text):
    #     try:
    #         response = client.chat_postMessage(
    #             channel=user_id,
    #             blocks=blocks,
    #             text=text
    #         )
    #     except SlackApiError as e:
    #         print(f"Error sending message: {e.response['error']}")
