import threading
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
):
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[email for email in recipient_list],
        bcc=bcc_list,  # Adding BCC support
    )


    if template:
        html_content = render_to_string(template, context)

        email.attach_alternative(html_content, "text/html")

    # start a thread for each email
    try:
        EmailThread(email).start()

    except ConnectionError:
        print("Something went wrong \nCouldn't send Email")