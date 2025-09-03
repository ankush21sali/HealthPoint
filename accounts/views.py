from django.shortcuts import render, redirect
from . models import ContactUs, Doctor, Patient, Department
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


# Create your views here.
def home(request):
    return render(request, "accounts/home.html")



def services(request):
    return render(request, "accounts/services.html")



def aboutus(request):
    return render(request, "accounts/aboutus.html")



def view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, "accounts/doctors.html", {'doctors': doctors})



def departments(request):
    departments = Department.objects.all()
    return render(request, "accounts/departments.html", {'departments': departments})



def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            contact = ContactUs(name=name, email=email, message=message)
            contact.save()
            messages.success(request, "Thank you for reaching out! Our team will contact you shortly.")
            return redirect('contactus')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, "accounts/contactus.html")



def loginpage(request):
    return render(request, "accounts/loginpage.html")



def patient_register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        blood_group = request.POST.get('blood_group')
        disease = request.POST.get('disease')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "accounts/patient_register.html")
        
        if not (first_name and last_name and gender and date_of_birth and blood_group and disease and email and contact and password ):
            messages.error(request, "All fields are required")
            return render(request, "accounts/patient_register.html")
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "accounts/patient_register.html")
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        Patient.objects.create(user=user, contact=contact, gender=gender, blood_group=blood_group, date_of_birth=date_of_birth, disease=disease)

        messages.success(request, "Registration successful! Please login.")
        return redirect('patient_login')
        

    return render(request, "accounts/patient_register.html")


def patient_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:

            if hasattr(user, "patient"):
                login(request, user)
                return redirect("patient_dashboard")
            else:
                messages.error(request, "You are not authorized as a Patient.")
                return redirect("patient_login")
            
        else:
            messages.error(request, "Invalid email or password")
            
    return render(request, "accounts/patient_login.html")



def doctor_register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        department = request.POST.get('department')
        specialist = request.POST.get('specialist')
        doctor_image = request.FILES.get('doctor_image')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "accounts/doctor_register.html")
        
        if not (first_name and last_name and gender and email and contact and password and department and specialist and doctor_image):
            messages.error(request, "All fields are required")
            return render(request, "accounts/doctor_register.html")
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "accounts/doctor_register.html")
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        Doctor.objects.create(user=user, gender=gender, contact=contact, department=department, specialist=specialist, doctor_image=doctor_image)
        messages.success(request, "Registration successful! Please login.")
        return redirect('doctor_login')

    return render(request, "accounts/doctor_register.html")

def doctor_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:

            if hasattr(user, "doctor"):
                login(request, user)
                return redirect("doctor_dashboard")
            else:
                messages.error(request, "You are not authorized as a Doctor.")
                return redirect("doctor_login")
            
        else:
            messages.error(request, "Invalid email or password")
            
    return render(request, "accounts/doctor_login.html")



def user_logout(request):
    logout(request)
    return redirect('home')



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "You are not authorized to access the admin dashboard.")
        
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/admin_login.html")