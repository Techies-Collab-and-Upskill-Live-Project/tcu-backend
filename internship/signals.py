from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal
from .models import InternshipApplication
from core.email_backend import send_email
from slackbot.utils import SlackBot
from decouple import config


@receiver(post_save, sender=InternshipApplication)
def send_application_email(sender, instance, created, **kwargs):
    if created:
        # Context for the email templates
        context = {
            'name': instance.full_name,
            'experience': instance.experience,
            'skill': instance.skill,
            'subject': 'We received your application',
            'email': instance.email,
            'applicant_link': f'https://www.tculive.com/application/{instance.id}',
        }

        # Send email to the applicant
        applicant_subject = 'We received your application'
        applicant_template = 'email/applicant.html'
        send_email(
            subject=applicant_subject,
            recipient_list=[instance.email],
            context=context,
            template=applicant_template
        )

        # Send email to the admin
        admin_subject = 'New Internship Application'
        admin_template = 'email/application_admin.html'
        send_email(
            subject=admin_subject,
            recipient_list=[],  # Empty TO list
            bcc_list=['ogboyesam@gmail.com', 'tculiveprojects@gmail.com'], 
            context=context,
            template=admin_template
        )

@receiver(post_save, sender=InternshipApplication)
def send_application_to_slack(sender, instance, created, **kwargs):
    if created and (config("ENVIRONMENT") == "production"):
        # Send Slack message to a channel
        slack_bot = SlackBot()
        slack_channel_name = config("SLACK_DEV_CHANNEL_ID")  
        slack_channel_id = slack_bot.get_channel_id(slack_channel_name)

        applicant_link = f'https://www.tculive.com/application/{instance.id}'
        message = (
            f"Hi Boss, we have a new Internship Application\n"
            f"Full Name: {instance.full_name}\n"
            f"Email: {instance.email}\n"
            f"Skill: {instance.skill}\n"
            f"Experience: {instance.experience}\n"
            f"More Details: {applicant_link}"
        )
        slack_bot.send_message_to_channel(slack_channel_id, message)

# Define a custom signal
internship_application_submitted = Signal()

@receiver(internship_application_submitted)
def send_internship_application_email(sender, name, email, **kwargs):
    # Your email sending logic here
    context = {
            'name': name,
        }
    send_acceptance_template = 'email/acceptance.html'
    
    send_email(
        subject='Congratulations...TCU2.0',
        recipient_list=[email],
        context=context,
        template=send_acceptance_template,
        attachments=['ProjectTimelines.pdf', 'TermsAndConditions.pdf']
    )
    print(f"Sent email to {name} at {email}")