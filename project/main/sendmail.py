from django.core.mail import send_mail, mail_admins
from django.conf import settings


def sendmail(theme, message, recipients):
    send_mail(theme, message, settings.EMAIL_HOST_USER, [recipients])


def sendmail_admins(theme, message):
    mail_admins(theme, message)
