from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Doctor, Patient
from patients.models import Appointment
from . models import Discharge, Billing
from . forms import BillingForm

# Create your views here.

@login_required
def doctor_dashboard(request):
    print(">>> Logged in user:", request.user.username)

    return render(request, 'doctors/doctor_dashboard.html')



@login_required
def our_patients(request):
    patients = Patient.objects.all()
    return render(request, 'doctors/our_patients.html', {'patients': patients})



@login_required
def discharge_list(request):
    discharge_lists = Discharge.objects.all()  
    return render(request, 'doctors/discharge_list.html', {'discharge_lists': discharge_lists})



@login_required
def discharge_form(request, id):
    doctor = get_object_or_404(Doctor, user=request.user)
    patient = get_object_or_404(Patient, patient_id=id)

    if request.method == "POST":
        discharge_date = request.POST.get('discharge_date')
        discharge_reason = request.POST.get('discharge_reason')

        if discharge_date and discharge_reason:
            discharge = Discharge.objects.create(doctor=doctor, patient=patient, discharge_date=discharge_date, discharge_reason=discharge_reason)

            # Patient Discharge Confirmation
            patient.is_discharge = True
            patient.save()

            discharge.save()

            return redirect('our_patients')

    return render(request, 'doctors/discharge_form.html')



@login_required
def view_details(request, id):
    patient_detail = get_object_or_404(Patient, patient_id=id)
    return render(request, 'doctors/view_details.html', {"patient_detail": patient_detail})



@login_required
def billing_form(request):
    if request.method == "POST":
        form = BillingForm(request.POST)

        if form.is_valid():
            billing = form.save(commit=False)
            billing.doctor = get_object_or_404(Doctor, user=request.user)
            billing.save()
            return redirect('your_patients')
    else:
        form = BillingForm()

    return render(request, 'doctors/billing_form.html', {'form': form})



@login_required
def your_patients(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    billings = Billing.objects.filter(doctor=doctor)
    return render(request, 'doctors/your_patients.html', {'billings': billings})