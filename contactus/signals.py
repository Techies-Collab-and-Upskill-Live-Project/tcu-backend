from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ContactUs
from core.email_backend import send_email
from slackbot.utils import SlackBot
from decouple import config


@receiver(post_save, sender=ContactUs)
def send_contact_emails(sender, instance, created, **kwargs):
    if created:
        context = {
            'name': instance.name, 
            'message': instance.message,
            'enquiry_type': instance.enquiry_type,
            'subject': instance.subject,
            'email': instance.email
        }
        
        # Send email to the person who submitted the form
        subject = 'We received your enquiry'
        recipient_list = [instance.email]
        template = 'email/contact_sender.html'
        
        # Send email to Admin
        admin_subject = 'New Enquiry'
        admin_template = 'email/contact_admin.html'
        admin_email = ['ogboyesam@gmail.com', 'tculiveprojects@gmail.com']
        
        send_email(subject=subject, recipient_list=recipient_list, context=context, template=template)
        send_email(subject=admin_subject, recipient_list=[], bcc_list=admin_email, context=context, template=admin_template)


@receiver(post_save, sender=ContactUs)
def send_application_to_slack(sender, instance, created, **kwargs):
    if created:
        # Send Slack message to a channel
        slack_bot = SlackBot()
        slack_channel_name = config("SLACK_DEV_CHANNEL_ID")  
        slack_channel_id = slack_bot.get_channel_id(slack_channel_name)

        message = (
            f"Hi Boss, we have a new Enquiry\n"
            f"Full Name: {instance.name}\n"
            f"Email: {instance.email}\n"
            f"Subject: {instance.subject}\n"
            f"Message: {instance.message}\n\n"
            f"Please respond swiftly"
        )
        slack_bot.send_message_to_channel(slack_channel_id, message)
