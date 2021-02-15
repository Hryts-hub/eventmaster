from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    slug = models.SlugField(primary_key=True, verbose_name="slug")
    country_name = models.CharField(max_length=50)
    updated = models.BooleanField(default=True)

    def __str__(self):
        return self.country_name


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    TIME_ZONE = [
        ("0", 'Greenwich Mean time'),
        ("3", '3 hours'),
    ]
    offset = models.CharField(default="0", max_length=2, null=True, choices=TIME_ZONE)
    country: Country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name="users_country")
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and /./+/-/_ only. Do not use @.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
