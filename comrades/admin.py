from django.contrib import admin

from comrades.models import CustomUser, Country

admin.site.register(CustomUser)
admin.site.register(Country)