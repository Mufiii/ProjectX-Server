from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings
from vendor.models import ProjectProposal,Project

@shared_task
def send_email_task(selected_users_emails=None, project_id=None):
    project = Project.objects.filter(id=project_id)
    mail_subject = "Congratulations! You have been selected for the project"
    message = f"You have been selected for the project Congratulations!"
    
    send_mail(
        subject=mail_subject,
        message=message,
        from_email= settings.EMAIL_HOST_USER,
        recipient_list=selected_users_emails,
        fail_silently=True,
    )
    return "Done"
    