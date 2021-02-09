from django.db import models
from datetime import timedelta
from django.utils import timezone
from comrades.models import CustomUser, Country
import datetime


class Events(models.Model):
    # offset должено быть св-вом юзера и вписываться при регистрации, но пока что так...
    offset = datetime.timedelta(hours=3)

    DO_NOT_REMIND = ""
    REMINDER = [
        (DO_NOT_REMIND, 'do not remind'),
        ((timedelta(hours=1)), 'remind me in an hour'),
        ((timedelta(hours=2)), 'remind me in two hours'),
        ((timedelta(hours=4)), 'remind me in four hours'),
        ((timedelta(days=1)), 'remind me of the day'),
        ((timedelta(weeks=1)), 'remind me a week in advance'),
    ]
    event = models.CharField(max_length=250)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users_events')
    date_event = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(default='23:59', blank=True)
    remind = models.CharField(default=DO_NOT_REMIND, max_length=30, choices=REMINDER)
    time_to_remind = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.event} - {self.user}"

    def save(self, **kwargs):
        if self.remind:
            datetime_event = datetime.datetime.combine(self.date_event, self.start_time)
            self.time_to_remind = datetime_event - self.remind
            self.time_to_remind = timezone.make_aware(self.time_to_remind)
            self.time_to_remind = self.time_to_remind - self.offset
        super().save(**kwargs)


class Holidays(models.Model):
    holiday = models.CharField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_holidays")
    date = models.DateField()
    duration = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.holiday} - {self.country}"
