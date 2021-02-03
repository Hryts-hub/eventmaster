from django.db import models

from comrades.models import CustomUser


class Events(models.Model):
    event = models.CharField(max_length=250)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users_events')
    date_event = models.DateField()
    start_time = models.TimeField(default='00:00')
    end_time = models.TimeField(default='23:59')