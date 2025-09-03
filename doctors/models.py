from django.db import models
from accounts.models import Patient, Doctor

# Create your models here.

class Discharge(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    discharge_date = models.DateField()
    discharge_reason = models.TextField(max_length=200)

    def __str__(self):
        return f'{self.patient.user.first_name} {self.patient.user.last_name} Is Discharged By Dr.{self.doctor.user.first_name} {self.doctor.user.last_name}'
    


class Billing(models.Model):

    STATUS_CHOICES = [
        ("Paid", 'paid'),
        ("Unpaid", 'unpaid'),
        ("Pending", "pending"),
        ("Cancelled", "cancelled"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_date = models.DateField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES)
    description = models.TextField(max_length=250)

    def __str__(self):
        return f'Total Amount Billed: ₹{self.amount}'