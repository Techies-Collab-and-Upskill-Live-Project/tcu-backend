# load_data/management/commands/load_applications.py
import json
from django.core.management.base import BaseCommand
from internship.models import InternshipApplication  # Replace with your actual app name

# python manage.py load_applications 
# to run this command
class Command(BaseCommand):
    help = 'Load applications from JSON file into SQLite database'

    def handle(self, *args, **kwargs):
        with open('applications.json', 'r') as json_file:
            applications = json.load(json_file)

        for app_data in applications['applications']:
            InternshipApplication.objects.create(
                id=app_data['id'],
                certificate=app_data['certificate'],
                date_created=app_data['date_created'],
                date_updated=app_data['date_updated'],
                email=app_data['email'],
                full_name=app_data['full_name'],
                twitter_handle=app_data['twitter_handle'],
                linkedin=app_data['linkedin'],
                skill=app_data['skill'],
                experience=app_data['experience'],
                about_skill=app_data['about_skill'],
                commitment=app_data['commitment'],
                birthdate=app_data['birthdate'],
            )

        self.stdout.write(self.style.SUCCESS('Applications loaded successfully'))
