from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings
from vendor.models import ProjectProposal


@shared_task
def send_emails_to_selected_users():
    applicants = ProjectProposal.objects.filter

@shared_task
def send_email_task(recipient_email, subject, message):

    send_mail(
        subject=subject,
        message=message,
        from_email= settings.EMAIL_HOST_USER,
        to=[recipient_email],
        fail_silently=False,
    )
    