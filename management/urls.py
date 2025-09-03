from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),
    path("manage_department/", views.manage_department, name="manage_department"),
    path("department_form/", views.department_form, name="department_form"),
    path("edit_department/<int:id>", views.edit_department, name="edit_department"),

    path("manage_patients/", views.manage_patients, name="manage_patients"),
    path("add_patient/", views.add_patient, name="add_patient"),
    path("edit_patient/<int:id>", views.edit_patient, name="edit_patient"),

    path("manage_doctors/", views.manage_doctors, name="manage_doctors"),
    path("add_doctor/", views.add_doctor, name="add_doctor"),
    path("edit_doctor/<int:id>", views.edit_doctor, name="edit_doctor"),

    path("manage_appointments/", views.manage_appointments, name="manage_appointments"),
    path("add_appointment/", views.add_appointment, name="add_appointment"),
    path("edit_appointment/<int:id>", views.edit_appointment, name="edit_appointment"),

    path("manage_billings/", views.manage_billings, name="manage_billings"),
    path("add_billings/", views.add_billings, name="add_billings"),
    path("edit_billing/<int:id>", views.edit_billing, name="edit_billing"),

]
