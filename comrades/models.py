# from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser  #, BaseUserManager
# from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin


class Country(models.Model):
    country = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return f"{self.country}"


class CustomUser(AbstractUser):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)

#
#
# class MyUserManager(BaseUserManager):
#     def _create_user(self, username, email, password, **extra_fields):
#         if not username:
#             raise ValueError('The username must be set')
#         if not email:
#             raise ValueError('The email must be set')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_user(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(username, email, password, **extra_fields)
#
#     def create_superuser(self, username, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self._create_user(username, email, password, **extra_fields)
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(db_index=True, max_length=255, unique=True)
#     email = models.EmailField(validators=[validators.validate_email], unique=True, blank=False)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name="users_country")
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ('username',)
#     objects = MyUserManager()
#
#     def __str__(self):
#         return self.username
#
#     def get_full_name(self):
#         return self.username
#
#     def get_short_name(self):
#         return self.username
