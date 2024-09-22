from django.core.mail import send_mail
from django.conf import settings

def send_invite_email(to_email, subject, message):
    """
    Sends an email invitation to the specified email address.
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email], 
        fail_silently=False,
    )




