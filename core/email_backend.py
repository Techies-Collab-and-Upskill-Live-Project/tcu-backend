import threading
import os
import time
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
            print(f"Sent email to {self.email.to}")
        except Exception as e:
            print(f"Failed to send email: {e}")

def send_email(
    subject: str,
    recipient_list: list,
    message: str = None,
    context: dict = {},
    template: str = None,
    bcc_list: list = None,
    attachments: list = None,
):
    batch_size = 5
    for i in range(0, len(recipient_list), batch_size):
        batch = recipient_list[i:i + batch_size]
        threads = []
        
        for recipient in batch:
            email = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[recipient],
                bcc=bcc_list,  # Adding BCC support
            )

            if template:
                html_content = render_to_string(template, context)
                email.attach_alternative(html_content, "text/html")

            # Attach files if provided
            if attachments:
                for attachment in attachments:
                    file_path = os.path.join(settings.MEDIA_ROOT, 'attachments', attachment)
                    email.attach_file(file_path)

            # Create a new thread for each email
            thread = EmailThread(email)
            threads.append(thread)
            thread.start()

        # Wait for all threads in the batch to finish
        for thread in threads:
            thread.join()

        # Pause for 2 seconds between batches
        time.sleep(2)