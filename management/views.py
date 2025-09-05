from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.models import Patient, Doctor, Department
from patients.models import Appointment
from doctors.models import Billing
from django.db.models import Sum
from patients.forms import AdminAppointmentForm
from doctors.forms import AdminBillingForm

# Create your views here.
@login_required(login_url='/admin_login/')
def admin_dashboard(request):
    total_patient = Patient.objects.count()
    total_doctor = Doctor.objects.count()
    total_appointment = Appointment.objects.count()
    total_billing = Billing.objects.count()
    total_revenue = Billing.objects.aggregate(total=Sum('amount'))['total'] or 0

    data = {
        'total_patient': total_patient,
        'total_doctor': total_doctor,
        'total_appointment': total_appointment,
        'total_billing': total_billing,
        'total_revenue': total_revenue,
    }

    return render(request, 'management/admin_dashboard.html', {'data': data})



@login_required(login_url='/admin_login/')
def manage_department(request):
    departments = Department.objects.all()
    
    # Delete Department
    if request.method == "POST":
        delete_department = request.POST.get('delete_department')

        if delete_department:
            department = get_object_or_404(Department, id=delete_department)
            department.delete()
            messages.success(request, "Department successfully Deleted!")
            return redirect('manage_department')

    return render(request, 'management/manage_department.html', {'departments': departments})



@login_required(login_url='/admin_login/')
def department_form(request):
    if request.method == "POST":
        department_name = request.POST.get('department_name')
        description = request.POST.get('description')

        if department_name and description:
            new_department = Department.objects.create(department_name=department_name, description=description)
            new_department.save()
            return redirect('manage_department')

    return render(request, 'management/department_form.html')




@login_required(login_url='/admin_login/')
def edit_department(request, id):
    department = get_object_or_404(Department, id=id)

    if request.method == "POST":
        department_name = request.POST.get('department_name')
        description = request.POST.get('description')

        if department_name and description:

            department.department_name = department_name
            department.description = description
            department.save()
            messages.success(request, "Department updated successfully!")
            return redirect('manage_department')
        
        else:
            messages.error(request, "Both fields are required.")

    return render(request, 'management/edit_department.html', {'department': department})    




@login_required(login_url='/admin_login/')
def manage_patients(request):
    patients = Patient.objects.all()

    #Delete Patient
    if request.method == "POST":
        delete_btn = request.POST.get('delete_btn')

        if delete_btn:
            delete_patient = Patient.objects.get(patient_id=delete_btn)
            delete_patient.user.delete()
            messages.success(request, "Patient Info successfully Deleted!")
            return redirect('manage_patients')

    return render(request, 'management/manage_patients.html', {'patients': patients})




@login_required(login_url='/admin_login/')
def add_patient(request):
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
            return redirect('add_patient')
        
        if not (first_name and last_name and gender and date_of_birth and blood_group and disease and email and contact and password ):
            messages.error(request, "All fields are required")
            return redirect('add_patient')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('add_patient')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        Patient.objects.create(user=user, contact=contact, gender=gender, blood_group=blood_group, date_of_birth=date_of_birth, disease=disease)

        messages.success(request, "New Patient Added successful!")
        return redirect('manage_patients')
    
    return render(request, 'management/add_patient.html')



@login_required(login_url='/admin_login/')
def edit_patient(request, id):
    patient = get_object_or_404( Patient, patient_id=id)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        disease = request.POST.get('disease')
        email = request.POST.get('email')
        contact = request.POST.get('contact')


        if not (first_name and last_name and date_of_birth and disease and email and contact):
            messages.error(request, "All fields are required")
            return redirect('edit_patient', id=patient.patient_id)
        
        
        if User.objects.filter(username=email).exclude(id=patient.user.id).exists():
            messages.error(request, "Email already registered")
            return redirect('edit_patient', id=patient.patient_id)
        

        patient.user.first_name = first_name
        patient.user.last_name = last_name
        patient.user.email = email
        patient.user.username = email

        patient.date_of_birth = date_of_birth
        patient.disease = disease
        patient.contact = contact
        
        patient.user.save()
        patient.save()

        messages.success(request, "Patient updated successfully!")
        return redirect('manage_patients')


    return render(request, 'management/edit_patient.html', {'patient': patient})



@login_required(login_url='/admin_login/')
def manage_doctors(request):
    doctors = Doctor.objects.all()

    #Delete a Doctor
    if request.method == "POST":
        delete_btn = request.POST.get('delete_btn')
        if delete_btn:
            delete_doctor = Doctor.objects.get(doctor_id=delete_btn)
            delete_doctor.user.delete()
            messages.success(request, "Doctor Info successfully Deleted!")
            return redirect('manage_doctors')
        
    return render(request, 'management/manage_doctors.html', {'doctors': doctors})



@login_required(login_url='/admin_login/')
def add_doctor(request):
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
        is_active = request.POST.get('is_active')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('add_doctor')
        
        if not (first_name and last_name and gender and email and contact and password and department and specialist and doctor_image and is_active):
            messages.error(request, "All fields are required")
            return redirect('add_doctor')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('add_doctor')
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        if is_active == "True":
            is_active = True
        else:
            is_active = False

        Doctor.objects.create(user=user, gender=gender, contact=contact, department=department, specialist=specialist, doctor_image=doctor_image, is_active=is_active)
        messages.success(request, "New Doctor Added successful!")
        return redirect('manage_doctors')
    
    return render(request, 'management/add_doctor.html')



@login_required(login_url='/admin_login/')
def edit_doctor(request, id):
    doctor = get_object_or_404(Doctor, doctor_id=id)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        department = request.POST.get('department')
        specialist = request.POST.get('specialist')
        doctor_image = request.FILES.get('doctor_image')
        is_active = request.POST.get('is_active')

        
        if not (first_name and last_name and email and contact and department and specialist):
            messages.error(request, "All fields are required")
            return redirect('edit_doctor', id=doctor.doctor_id)
        
        if User.objects.filter(username=email).exclude(id=doctor.user.id).exists():
            messages.error(request, "Email already registered")
            return redirect('edit_doctor', id=doctor.doctor_id)
        
        doctor.user.first_name = first_name
        doctor.user.last_name = last_name
        doctor.user.email = email
        doctor.user.username = email

        doctor.contact = contact
        doctor.department = department
        doctor.specialist = specialist
        
        if doctor_image:
            doctor.doctor_image = doctor_image
        
        if is_active == "True":
            is_active = True
        else:
            is_active = False
        
        doctor.is_active = is_active

        doctor.user.save()
        doctor.save()
        
        messages.success(request, "Doctor updated successful!")
        return redirect('manage_doctors')

    return render(request, 'management/edit_doctor.html', {'doctor': doctor})



@login_required(login_url='/admin_login/')
def manage_appointments(request):
    appointments = Appointment.objects.all()

    if request.method == "POST":
        delete_btn = request.POST.get('delete_btn')

        if delete_btn:
            delete_appointment = Appointment.objects.get(id=delete_btn)
            delete_appointment.delete()
            messages.success(request, "Appointment successfully Deleted!")
            return redirect('manage_appointments')

    return render(request, 'management/manage_appointments.html', {'appointments': appointments})



@login_required(login_url='/admin_login/')
def add_appointment(request):
    if request.method == "POST":
        form = AdminAppointmentForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.save()
            messages.success(request, "Appointment Is Successfully Booked")
            return redirect('manage_appointments')
        else:
            messages.error(request, "Please Enter All The Required Fields")
            return redirect('manage_appointments')
    else:
        form = AdminAppointmentForm()
        
    return render(request, 'management/add_appointment.html', {'form': form})



@login_required(login_url='/admin_login/')
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == "POST":
        form = AdminAppointmentForm(request.POST, instance=appointment)

        if form.is_valid():
            form.save()
            messages.success(request, "Appointment Is Successfully Updated")
            return redirect('manage_appointments')
        else:
            messages.error(request, "Please Enter All The Required Fields")
            return redirect('manage_appointments')
        
    else:
        form = AdminAppointmentForm(instance=appointment)

    return render(request, 'management/edit_appointment.html', {'form': form})



@login_required(login_url='/admin_login/')
def manage_billings(request):
    billings = Billing.objects.all()

    if request.method == "POST":
        delete_btn = request.POST.get('delete_btn')

        if delete_btn:
            delete_bill = Billing.objects.get(id=delete_btn)
            delete_bill.delete()
            return redirect('manage_billings')

    return render(request, 'management/manage_billings.html', {'billings': billings})



@login_required(login_url='/admin_login/')
def add_billings(request):
    if request.method == "POST":
        form = AdminBillingForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Billing Is Successfully Added")
            return redirect('manage_billings')
        else:
            messages.error(request, "Please Enter All The Required Fields")
            return redirect('manage_billings')
        
    else:
        form = AdminBillingForm()

    return render(request, 'management/add_billings.html', {'form': form})



@login_required(login_url='/admin_login/')
def edit_billing(request, id):
    billing = get_object_or_404(Billing, pk=id)

    if request.method == "POST":
        form = AdminBillingForm(request.POST, instance=billing)

        if form.is_valid():
            form.save()
            messages.success(request, "Billing Is Successfully Updated")
            return redirect('manage_billings')
        
    else:
        form = AdminBillingForm(instance=billing)

    return render(request, 'management/edit_billing.html', {'form': form})