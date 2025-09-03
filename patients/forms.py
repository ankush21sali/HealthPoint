from django import forms
from accounts.models import Doctor, Patient
from . models import Appointment


class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label="Select Doctor", widget=forms.Select())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Appointment
        fields = ["doctor", "date", "time", "symptoms"]


class AdminAppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label="Select Doctor", widget=forms.Select())
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), empty_label="Select Patient", widget=forms.Select())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ["doctor", 'patient', "date", "time", "symptoms", 'status']