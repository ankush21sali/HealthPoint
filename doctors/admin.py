from django.contrib import admin
from . models import Discharge, Billing

# Register your models here.
@admin.register(Discharge)
class DischargeAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'discharge_date')
    list_per_page = 10
    search_fields = ('doctor', 'patient', 'discharge_date')
    list_filter = ('discharge_date',)
    readonly_fields = ('discharge_reason',)


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'amount', 'billing_date', 'status')
    list_editable = ('amount',)
    list_per_page = 10
    search_fields = ('doctor', 'patient', 'amount' 'status')
    readonly_fields = ('description',)
    list_filter = ('amount', 'billing_date', 'status')

