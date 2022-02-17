

from accounts.models import PasswordResetTokens
from django.core.mail import send_mail
from django.utils import timezone
from django_extensions.management.jobs import DailyJob, QuarterHourlyJob
from django.conf import settings

def updatePasswordResets(qs):
    try:
        qs.update(active=False)
        status = True
    except Exception:
        status = False
    return status


class Job(DailyJob):
    help = "Update Password Reset Tokens daily"

    def execute(self):
        timestamp_raw = timezone.now()
        date_format = "%Y-%m-%d %H:%M:%S"
        timestamp = timezone.datetime.strftime(timestamp_raw, date_format)
        salutation = f"QuarterHourly Cron Job runs at: {timestamp}"
        sTime = timezone.now()
        try:
            tokens = PasswordResetTokens.objects.filter(active=True)
            status = updatePasswordResets(tokens)
        except Exception as exp:
            status = f"An Error Occured. Error: {exp}"
        msg = f"{salutation}.\nSummary: {status}\n"

        eTime = timezone.now()
        msg = msg + f"Time Elapsed: {eTime - sTime}"
        print(f"{msg}")
        send_mail(
            subject="AREWA CINEMA | Password Tokens Reset - QuarterHourly Cron Job",
            message=msg,
            from_email=settings.SERVER_EMAIL,
            recipient_list=["ahmadabdulnasir9@gmail.com"],
            fail_silently=False,
        )
