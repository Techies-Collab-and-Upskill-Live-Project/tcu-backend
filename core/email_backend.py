import threading
import os
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        super().__init__(group=None)

    def run(self):
        try:
            self.email.send()
            logging.info(f"Sent email to {self.email.to}")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")

def send_email(
    subject: str,
    recipient_list: list,
    message: str = None,
    context: dict = {},
    template: str = None,
    bcc_list: list = None,
    attachments: list = None,
):
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email for email in recipient_list],
        bcc=bcc_list,
        reply_to=[settings.EMAIL_HOST_USER],
    )


    if template:
        html_content = render_to_string(template, context)

        email.attach_alternative(html_content, "text/html")
    
    # Handle attachments if provided
    if attachments:
        for attachment_path in attachments:
            if os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as f:
                    filename = os.path.basename(attachment_path)
                    email.attach(filename, f.read(), 'application/pdf')
            else:
                logging.info(f"Attachment not found: {attachment_path}")

    # start a thread for each email
    try:
        EmailThread(email).start()

    except ConnectionError as e:
        logging.error(f"Something went wrong \nCouldn't send Email: {e}")