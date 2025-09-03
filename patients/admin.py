from django.contrib import admin
from . models import Appointment

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display =  ('patient', 'date', 'time', 'doctor')
    list_editable = ('doctor', 'date', 'time')
    list_per_page = 10
    search_fields = ('patient', 'date', 'time', 'doctor')
    ordering = ('date', 'time')