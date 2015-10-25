from django.contrib import admin
from events.models import Event, Attendance

# Register your models here.
#default site is admin.site.register

admin.site.register(Event)
admin.site.register(Attendance)
