from django.contrib import admin

from events.models import Events, Holidays

admin.site.register(Events)
admin.site.register(Holidays)
