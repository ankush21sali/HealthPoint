from django.urls import path
from . import views

urlpatterns = [
    path("", views.doctor_dashboard, name="doctor_dashboard"),
    path("our_patients/", views.our_patients, name="our_patients"),
    path("discharge_list/", views.discharge_list, name="discharge_list"),
    path("discharge_form/<int:id>", views.discharge_form, name="discharge_form"),
    path("view_details/<int:id>", views.view_details, name="view_details"),
    path("billing_form/", views.billing_form, name="billing_form"),
    path("your_patients/", views.your_patients, name="your_patients"),
]
