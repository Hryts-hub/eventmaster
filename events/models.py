from django.db import models
from datetime import timedelta
from django.utils import timezone
from comrades.models import CustomUser, Country
import datetime


class Events(models.Model):

    REMINDER = [
        ("0", 'Do not remind'),
        ("3600", '1 hour'),
        ("7200", '2 hours'),
        ("14400", '4 hours'),
        ("86400", '1 day'),
        ("604800", '1 week'),
    ]

    event = models.CharField(max_length=250)
    user: CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users_events')
    date_event = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(default='23:59', blank=True)
    remind = models.CharField(default="0", max_length=30, choices=REMINDER)
    time_to_remind = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.event} - {self.user}"

    def save(self, **kwargs):
        if self.remind:
            datetime_event = datetime.datetime.combine(self.date_event, self.start_time)
            rem = timedelta(seconds=int(str(self.remind)))
            self.time_to_remind = timezone.make_aware(datetime_event - rem)
            offset = timedelta(hours=int(self.user.offset))
            if offset:
                self.time_to_remind = self.time_to_remind - offset
        super().save(**kwargs)


class Holidays(models.Model):
    holiday = models.CharField(max_length=250)
    country: Country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_holidays")
    date = models.DateField()
    duration = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    updated = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.holiday} - {self.country}"
