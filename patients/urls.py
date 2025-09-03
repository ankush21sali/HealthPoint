from django.urls import path
from . import views

urlpatterns = [
    path("", views.patient_dashboard, name="patient_dashboard"),
    path("our_departments/", views.our_departments, name="our_departments"),
    path("our_doctors/", views.our_doctors, name="our_doctors"),
    path("booknow/", views.booknow, name="booknow"),
    path("appointments/", views.appointments, name="appointments"),
    path("edit_appointments/<int:id>", views.edit_appointments, name="edit_appointments"),
    path("billings/", views.billings, name="billings"),
]
