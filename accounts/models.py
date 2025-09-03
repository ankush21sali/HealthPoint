from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Patient(models.Model):

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    patient_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10, default='patient', editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15, blank=False, null=False)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')), blank=True, null=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    disease = models.TextField(max_length=250, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_discharge = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user.username} (Patient)'
    

class Doctor(models.Model):

    DEPARTMENTS_CHOICES = [
    ('cardiologist', 'Cardiologist'),
    ('dermatologist', 'Dermatologist'),
    ('neurologist', 'Neurologist'),
    ('pediatrician', 'Pediatrician'),
    ('gynecologist', 'Gynecologist'),
    ('orthopedic', 'Orthopedic'),
    ('psychiatrist', 'Psychiatrist'),
    ('radiologist', 'Radiologist'),
    ('general_physician', 'General Physician'),
    ('ent_specialist', 'ENT Specialist'),
    ]


    doctor_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10, default="doctor", editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15, blank=False, null=False)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')), blank=True, null=True)
    department = models.CharField(max_length=20, choices=DEPARTMENTS_CHOICES, default='General Physician')
    specialist = models.TextField(max_length=100, blank=True, null=True)
    doctor_image = models.ImageField(upload_to='doctor_image/')
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return f'Dr.{self.user.username} (Doctor)'
    



class Department(models.Model):
    department_name = models.CharField(max_length=50, default="")
    description = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.department_name




class ContactUs(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField(max_length=250)

    def __str__(self):
        return self.name
    

