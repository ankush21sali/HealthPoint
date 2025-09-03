from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("view_doctors/", views.view_doctors, name="view_doctors"),
    path("departments/", views.departments, name="departments"),
    path("contactus/", views.contactus, name="contactus"),
    path("loginpage/", views.loginpage, name="loginpage"),

    # Doctors Authentication urls
    path("doctor_register/", views.doctor_register, name="doctor_register"),
    path("doctor_login/", views.doctor_login, name="doctor_login"),
    path('doctors/', include("doctors.urls")),

    # Patient Authentication urls
    path("patient_register/", views.patient_register, name="patient_register"),
    path("patient_login/", views.patient_login, name="patient_login"),
    path('patients/', include("patients.urls")),

    #Logout For All Admin, Doctor and Patient
    path("user_logout/", views.user_logout, name="user_logout"),

    # Admin Authentication urls
    path("admin_login/", views.admin_login, name="admin_login"),
    path('management/', include("management.urls")),
]
