from django.db import models
from django.utils import timezone
from accounts.models import Patient, Doctor

# Create your models here.

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField()
    symptoms = models.TextField(max_length=250)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("completed", "Completed"), ("confirmed", "Confirmed")], default="pending")

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.date} at {self.time}"