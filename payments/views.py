# payments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from students.models import BusPass
from django.contrib import messages
from datetime import date, timedelta
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from students.models import BusPass



def payment_verification(request):
    if request.method == 'POST':
        entered_id = request.POST.get('approval_id')

        try:
            bus_pass = BusPass.objects.get(
                approval_id=entered_id,
                student__user=request.user,
                status='approved'
            )

            request.session['bus_pass_id'] = bus_pass.id

            return redirect('select_plan')

        except BusPass.DoesNotExist:
            messages.error(
                request,
                "Invalid Approval ID or application not approved yet."
            )

    return render(
        request,
        'payments/payment.html'
    )


def select_plan(request):
    return render(
        request,
        'payments/select_plan.html'
    )


def payment_gateway(request, plan_name, amount):
    bus_pass_id = request.session.get('bus_pass_id')

    if not bus_pass_id:
        return redirect('payment')

    bus_pass = get_object_or_404(
        BusPass,
        id=bus_pass_id
    )

    context = {
        'selected_plan': plan_name,
        'amount': amount,
    }

    if request.method == 'POST':

        bus_pass.payment_status = 'completed'
        bus_pass.final_pass_generated = True
        bus_pass.amount = amount

        # New Application Flow
        if not bus_pass.renewal_requested:
            bus_pass.start_date = date.today()

            if plan_name == "1 Month":
                bus_pass.end_date = date.today() + timedelta(days=30)

            elif plan_name == "2 Months":
                bus_pass.end_date = date.today() + timedelta(days=60)

            elif plan_name == "6 Months":
                bus_pass.end_date = date.today() + timedelta(days=180)

        # Renewal Flow
        else:
            if plan_name == "1 Month":
                bus_pass.end_date = bus_pass.end_date + timedelta(days=30)

            elif plan_name == "2 Months":
                bus_pass.end_date = bus_pass.end_date + timedelta(days=60)

            elif plan_name == "6 Months":
                bus_pass.end_date = bus_pass.end_date + timedelta(days=180)

            bus_pass.renewal_requested = False

        bus_pass.save()

        request.session['selected_plan'] = plan_name

        messages.success(
            request,
            "Payment successful. Final E-Pass generated."
        )

        return redirect('final_pass')

    if is_mobile(request):
        return render(
            request,
            'payments/mobile_payment.html',
            context
        )
    else:
        return render(
            request,
            'payments/desktop_payment.html',
            context
        )


def final_pass(request):
    bus_pass_id = request.session.get('bus_pass_id')

    if not bus_pass_id:
        return redirect('payment')

    bus_pass = get_object_or_404(
        BusPass,
        id=bus_pass_id
    )

    selected_plan = request.session.get(
        'selected_plan',
        'Bus Pass Plan'
    )

    context = {
        'bus_pass': bus_pass,
        'selected_plan': selected_plan,
    }

    return render(
        request,
        'payments/final_pass.html',
        context
    )


def is_mobile(request):
    user_agent = request.META.get(
        'HTTP_USER_AGENT',
        ''
    ).lower()

    mobile_keywords = [
        'android',
        'iphone',
        'ipad',
        'mobile'
    ]

    return any(
        word in user_agent
        for word in mobile_keywords
    )


def download_pass(request):
    bus_pass = BusPass.objects.get(student__user=request.user)

    html = render_to_string('payments/final_pass.html', {
        'bus_pass': bus_pass,
        'selected_plan': request.session.get('selected_plan')
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bus_pass.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response