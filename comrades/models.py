from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    country = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return f"{self.country}"


class CustomUser(AbstractUser):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
