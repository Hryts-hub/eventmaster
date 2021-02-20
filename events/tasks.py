from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import send_mail
from events.models import Events
from django.conf import settings
from django.utils import timezone
from events.services import update_holidays


@shared_task()
def remind_event():
    try:
        t = timezone.make_aware(datetime.now())
        first_date = t - timedelta(minutes=5)
        last_date = t + timedelta(minutes=10)
        events = Events.objects.filter(time_to_remind__range=(first_date, last_date))
        i = 0
        for event in events:
            subject = f'{event.user.username}, Hello from eventmaster! '
            message = f'Your event  --- {event.event} ---.  ' \
                      f'Date: {event.date_event},  {event.start_time} - {event.end_time}.'
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [event.user.email]
            )
            i += 1
            Events.objects.filter(id=event.id).update(time_to_remind=None)
        print(f"Mails sent: {i}.")

    except Exception as e:
        print(f"remind ERROR: {e}")
        pass


@shared_task()
def refresh_holidays():
    update_holidays()
