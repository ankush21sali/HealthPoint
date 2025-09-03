from django import forms
from . models import Billing
from accounts.models import Doctor, Patient

class BillingForm(forms.ModelForm):

    STATUS_CHOICES = [
        ("Paid", 'paid'),
        ("Unpaid", 'unpaid'),
        ("Pending", "pending"),
        ("Cancelled", "cancelled"),
    ]


    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), empty_label="Select Patient", widget=forms.Select())
    billing_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Billing
        fields = ['patient', 'amount', 'billing_date', 'status', 'description']




class AdminBillingForm(forms.ModelForm):

    ADMIN_STATUS_CHOICES = [
        ("Paid", 'paid'),
        ("Unpaid", 'unpaid'),
        ("Pending", "pending"),
        ("Cancelled", "cancelled"),
    ]


    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label="Select Doctor", widget=forms.Select())
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), empty_label="Select Patient", widget=forms.Select())
    billing_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(choices=ADMIN_STATUS_CHOICES)

    class Meta:
        model = Billing
        fields = '__all__'