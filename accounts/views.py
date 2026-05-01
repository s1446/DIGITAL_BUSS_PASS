from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from notifications.models import Notification
from .forms import StudentRegisterForm
from students.models import BusPass
import random


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import StudentRegisterForm


def register_view(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(
                request,
                "Registration successful. Welcome!"
            )

            login(request, user)
            return redirect('student_dashboard')

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    else:
        form = StudentRegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Basic validation
        if not username or not password:
            messages.error(request, "Both fields are required.")
            return render(request, 'accounts/login.html')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            messages.success(request, "Login successful.")

            # Role-based redirect
            if user.is_superuser:
                return redirect('admin_dashboard')

            if hasattr(user, 'role'):
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'student':
                    return redirect('student_dashboard')

            return redirect('student_dashboard')

        else:
            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect('login')


def student_dashboard(request):
    return render(
        request,
        'students/dashboard.html'
    )


def admin_dashboard(request):
    total_applications = BusPass.objects.count()

    pending_applications = BusPass.objects.filter(
        status='pending'
    ).count()

    approved_applications = BusPass.objects.filter(
        status='approved'
    ).count()

    rejected_applications = BusPass.objects.filter(
        status='rejected'
    ).count()

    renewal_requests = BusPass.objects.filter(
        renewal_requested=True
    ).count()

    payment_completed = BusPass.objects.filter(
        payment_status='completed'
    ).count()

    all_applications = BusPass.objects.select_related(
        'student'
    ).order_by('-created_at')

    context = {
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'renewal_requests': renewal_requests,
        'payment_completed': payment_completed,
        'all_applications': all_applications,
    }

    return render(
        request,
        'adminpanel/dashboard.html',
        context
    )


def view_application(request, bus_pass_id):
    bus_pass = get_object_or_404(
        BusPass,
        id=bus_pass_id
    )

    return render(
        request,
        'adminpanel/application_details.html',
        {'bus_pass': bus_pass}
    )


def approve_application(request, bus_pass_id):
    bus_pass = get_object_or_404(
        BusPass,
        id=bus_pass_id
    )

    bus_pass.status = 'approved'

    if not bus_pass.approval_id:
        bus_pass.approval_id = "APR" + str(
            random.randint(10000, 99999)
        )

    bus_pass.save()

    Notification.objects.create(
        user=bus_pass.student.user,
        message=(
            f"Your application has been approved. "
            f"Approval ID: {bus_pass.approval_id}. "
            f"Please proceed to payment."
        )
    )

    return redirect('admin_dashboard')


def reject_application(request, bus_pass_id):
    bus_pass = get_object_or_404(
        BusPass,
        id=bus_pass_id
    )

    bus_pass.status = 'rejected'
    bus_pass.save()

    Notification.objects.create(
        user=bus_pass.student.user,
        message=(
            "Your application has been rejected. "
            "Please re-apply with correct details."
        )
    )

    return redirect('admin_dashboard')