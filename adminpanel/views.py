from django.shortcuts import render
from students.models import BusPass


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

    context = {
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'renewal_requests': renewal_requests,
        'payment_completed': payment_completed,
    }

    return render(
        request,
        'adminpanel/dashboard.html',
        context
    )