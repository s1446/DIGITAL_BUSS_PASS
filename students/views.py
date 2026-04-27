# students/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentProfileForm
from .forms import GovernmentEmployeeForm
from .forms import NonGovernmentEmployeeForm
from .forms import CitizenForm
from .forms import PWDForm

from .models import BusPass, StudentProfile

from datetime import date, timedelta
import random


def apply_bus_pass(request):
    """
    Always open the form page.
    Student can edit/reuse existing profile.
    Only one BusPass is created per student.
    """

    existing_student = StudentProfile.objects.filter(
        user=request.user
    ).first()

    if request.method == 'POST':
        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=existing_student
        )

        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()

            existing_bus_pass = BusPass.objects.filter(
                student=student
            ).first()

            if not existing_bus_pass:
                pass_number = "BP" + str(
                    random.randint(10000, 99999)
                )

                BusPass.objects.create(
                    student=student,
                    pass_number=pass_number,
                    start_date=date.today(),
                    end_date=date.today() + timedelta(days=30),
                    amount=500,
                    status='pending',
                    payment_status='pending',
                    final_pass_generated=False
                )

            return redirect('student_dashboard')

    else:
        form = StudentProfileForm(
            instance=existing_student
        )

    return render(
        request,
        'students/apply_pass.html',
        {'form': form}
    )


def check_status(request):
    bus_pass = BusPass.objects.filter(
        student__user=request.user
    ).first()

    return render(
        request,
        'students/status.html',
        {'bus_pass': bus_pass}
    )


def request_renewal(request):
    bus_pass = get_object_or_404(
        BusPass,
        student__user=request.user
    )

    # Keep same approval ID forever
    # Keep same pass number forever

    bus_pass.renewal_requested = True
    bus_pass.payment_status = 'pending'
    bus_pass.final_pass_generated = False

    bus_pass.save()

    # Directly move to payment using same pass
    request.session['bus_pass_id'] = bus_pass.id

    return redirect('select_plan')


def select_pass_type(request):
    return render(
        request,
        'students/select_pass_type.html'
    )


def government_employee_apply(request):
    if request.method == 'POST':
        form = GovernmentEmployeeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()

            return redirect('student_dashboard')

    else:
        form = GovernmentEmployeeForm()

    return render(
        request,
        'students/government_employee_form.html',
        {'form': form}
    )


def non_government_employee_apply(request):
    if request.method == 'POST':
        form = NonGovernmentEmployeeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()

            return redirect('student_dashboard')

    else:
        form = NonGovernmentEmployeeForm()

    return render(
        request,
        'students/non_government_employee_form.html',
        {'form': form}
    )


def citizen_apply(request):
    if request.method == 'POST':
        form = CitizenForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            citizen = form.save(commit=False)
            citizen.user = request.user
            citizen.save()

            return redirect('student_dashboard')

    else:
        form = CitizenForm()

    return render(
        request,
        'students/citizen_form.html',
        {'form': form}
    )


def pwd_apply(request):
    if request.method == 'POST':
        form = PWDForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            pwd = form.save(commit=False)
            pwd.user = request.user
            pwd.save()

            return redirect('student_dashboard')

    else:
        form = PWDForm()

    return render(
        request,
        'students/pwd_form.html',
        {'form': form}
    )