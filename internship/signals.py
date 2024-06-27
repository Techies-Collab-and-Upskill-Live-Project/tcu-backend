from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InternshipApplication
from core.email_backend import send_email

@receiver(post_save, sender=InternshipApplication)
def send_application_email(sender, instance, created, **kwargs):
    if created:
        # Context for the email templates
        context = {
            'name': instance.full_name,
            'message': instance.experience,
            'enquiry_type': instance.skill,
            'subject': 'We received your application',
            'email': instance.email
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
        admin_template = 'email/contact_admin.html'
        send_email(
            subject=admin_subject,
            # recipient_list=['ogboyesam@gmail.com', 'clintonebuka75@gmail.com', 'webrin2005@gmail.com', 'atesunate150@gmail.com'],  # Replace with your admin email
            recipient_list=['ogboyesam@gmail.com'],  # Replace with your admin email

            context=context,
            template=admin_template
        )

