from django.contrib import admin
from . models import Patient, Doctor, ContactUs, Department
from patients.models import Appointment

# Register your models here.
class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'user', 'department', 'contact', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('department', 'gender',)
    list_per_page = 10
    ordering = ('doctor_id',)
    search_fields = ('doctor_id', 'department', 'user', 'contact')
    readonly_fields = ('date_joined',)
    inlines = [AppointmentInline]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'user', 'contact', 'is_discharge')
    list_editable = ('is_discharge',)
    list_filter = ('blood_group', 'gender',)
    list_per_page = 10
    ordering = ('patient_id',)
    search_fields = ('patient_id', 'contact', 'user')
    readonly_fields = ('date_joined',)



@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)



admin.site.register(Department)