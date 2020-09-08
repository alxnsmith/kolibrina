from django.core.mail import send_mail
from django.conf import settings


def sendmail(theme, message, recipients):
    send_mail(theme, message, settings.EMAIL_HOST_USER, [recipients], fail_silently=False)
