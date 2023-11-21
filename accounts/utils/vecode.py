from django.core.mail import EmailMessage
from django.conf import settings


def send_email(data):
    try:
        email = EmailMessage(
            data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
            from_email=settings.EMAIL_HOST_USER
        )
        email.send()
        print("email send success")
    except Exception as e:
        return f"Email sending failed: {str(e)}"