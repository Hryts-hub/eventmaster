from django.db import models

from comrades.models import CustomUser, Country


class Events(models.Model):
    event = models.CharField(max_length=250)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users_events')
    date_event = models.DateField()
    start_time = models.TimeField(default='00:00')
    end_time = models.TimeField(default='23:59')

    def __str__(self):
        return f"{self.event} - {self.user}"


class Holidays(models.Model):
    holiday = models.CharField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_holidays")
    date = models.DateField()
    duration = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.holiday} - {self.country}"
