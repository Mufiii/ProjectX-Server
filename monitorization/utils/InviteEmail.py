from django.conf import settings
from django.core.mail import EmailMessage


def Invitation_send_email(data):
    try:
        email = EmailMessage(
            data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
            from_email= data["from_email"]
        )
        email.send()
        return True
    except Exception as e:
        return False
