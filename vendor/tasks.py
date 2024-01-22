import logging
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
logger = logging.getLogger(__name__)
from vendor.models import Project, ProjectProposal


@shared_task
def send_email_task(selected_users_emails=None, project_id=None):
    logger.info(f"Executing send_email_task with project_id: {project_id}")
    project = Project.objects.filter(id=project_id)
    mail_subject = "Congratulations! You have been selected for the project"
    message = f"You have been selected for the project Congratulations!"
    print("=============================================================================")
    print(selected_users_emails,project_id,'===================================================')

    # send_mail(
    #     subject=mail_subject,
    #     message=message,
    #     from_email=settings.EMAIL_HOST_USER,
    #     recipient_list=selected_users_emails,
    #     fail_silently=True,
    # )
    logger.info("Task completed successfully")
    return "Done"
