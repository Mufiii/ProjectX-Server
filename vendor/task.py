from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings
from vendor.views import DeveloperSkillsMatchingAPIView

def send_emails_to_selected_users():
    # Fetch the matching results from the API view
    view = DeveloperSkillsMatchingAPIView()
    print(view)
    response = view.get(None, project_id, threshold_score)
    matching_results = response.data['data']

    # Send emails to the selected users
    for result in matching_results:
        user_email = result['key']
        email_content = f"Congratulations! You have been selected for Project."

        send_mail.delay(email_content, user_email)


@shared_task
def send_mail(email_content, recipient_email):

    send_mail(
        subject="Important Message",
        message=email_content,
        from_email= settings.EMAIL_HOST_USER,
        to=[recipient_email],
        fail_silently=False,
    )
    