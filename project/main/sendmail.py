from .tasks import sendmail_task, sendmail_admins_task


def sendmail(theme, message, recipients):
    sendmail_task.delay(theme, message, recipients)


def sendmail_admins(theme, message):
    sendmail_admins_task.delay(theme, message)
