from django.conf import settings
from django.core.mail import send_mail

def send_email_if_required(subject:str, message:str) -> bool:
    if settings.EMAIL_NOTIFY:
        if settings.DEBUG:
            print("Sending email")
        res = send_mail(
            subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_RECEIVER],
            fail_silently=True
        )
        if res < 0:
            print("Something went wrong, couldn't send email!")
        else:
            return True
    else:
        if settings.DEBUG:
            print("Did not send email")
        return False