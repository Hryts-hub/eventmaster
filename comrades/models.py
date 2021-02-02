# from importlib._common import _

from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    country_name = models.CharField(primary_key=True, max_length=30)

    def __str__(self):
        return self.country_name


class CustomUser(AbstractUser):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name="users_country")
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
