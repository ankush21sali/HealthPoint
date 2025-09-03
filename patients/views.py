from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import AppointmentForm
from . models import Appointment
from accounts.models import Patient, Doctor, Department
from doctors.models import Billing


# Create your views here.

@login_required
def patient_dashboard(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time')
    return render(request, 'patients/patient_dashboard.html', {"appointments": appointments})


@login_required
def our_departments(request):
    departments = Department.objects.all()
    return render(request, 'patients/departments.html', {'departments': departments})


@login_required
def our_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'patients/doctors.html', {'doctors': doctors})


@login_required
def booknow(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.patient = get_object_or_404(Patient, user=request.user)
            booking.save()
            messages.success(request, "Appointment Is Successfully Booked")
            return redirect('appointments')
        else:
            messages.error(request, "Please Enter All The Required Fields")
            
    else:
        form = AppointmentForm()
        
    return render(request, 'patients/booknow.html', {'form': form})


@login_required
def appointments(request):
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time')

    if request.method == "POST":
        delete_id = request.POST.get('delete')
        appointment = get_object_or_404(Appointment, id=delete_id)
        appointment.delete()
        return redirect('appointments')

    return render(request, 'patients/appointments.html', {"appointments": appointments})


@login_required
def edit_appointments(request, id):
    appointment = get_object_or_404(Appointment, pk=id, patient=request.user.patient)

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments')
    
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'patients/edit_appointment.html', {"form": form, "appointment": appointment})



@login_required
def billings(request):
    patient = Patient.objects.get(user=request.user)
    bills = Billing.objects.filter(patient=patient) 

    return render(request, 'patients/billings.html', {'bills': bills})
