from celery import shared_task
from django.core.mail import send_mail, mail_admins
from django.conf import settings


@shared_task
def sendmail_task(theme, message, recipients):
    send_mail(theme, message, settings.EMAIL_HOST_USER, [recipients])


@shared_task
def sendmail_admins_task(theme, message):
    mail_admins(theme, message)
    sendmail_admins(theme, message)
