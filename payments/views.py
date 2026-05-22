# payments/views.py

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from students.models import BusPass

from datetime import (
    date,
    timedelta
)

from django.http import HttpResponse

from django.template.loader import render_to_string

from xhtml2pdf import pisa


# ==========================================
# PAYMENT VERIFICATION
# ==========================================

@login_required
def payment_verification(request):

    if request.method == 'POST':

        entered_id = request.POST.get('approval_id')

        try:

            # Find only current user's approved pass

            bus_pass = BusPass.objects.get(
                approval_id=entered_id,
                student__user=request.user,
                status='approved'
            )

            # ❌ Already paid

            if bus_pass.payment_status == 'completed':

                messages.error(
                    request,
                    "Payment already completed."
                )

                return redirect('payment')

            # ❌ Final pass already generated

            if bus_pass.final_pass_generated:

                messages.error(
                    request,
                    "Bus pass already generated."
                )

                return redirect('payment')

            # ✅ Save session

            request.session['bus_pass_id'] = bus_pass.id

            return redirect('select_plan')

        except BusPass.DoesNotExist:

            messages.error(
                request,
                "Invalid Approval ID or application not approved yet."
            )

            return redirect('payment')

    return render(
        request,
        'payments/payment.html'
    )


# ==========================================
# SELECT PLAN
# ==========================================

@login_required
def select_plan(request):

    bus_pass_id = request.session.get('bus_pass_id')

    if not bus_pass_id:
        return redirect('payment')

    return render(
        request,
        'payments/select_plan.html'
    )


# ==========================================
# PAYMENT GATEWAY
# ==========================================

@login_required
def payment_gateway(request, plan_name, amount):

    bus_pass_id = request.session.get('bus_pass_id')

    if not bus_pass_id:
        return redirect('payment')

    # Secure current user check

    bus_pass = get_object_or_404(
        BusPass,
        id=bus_pass_id,
        student__user=request.user
    )

    context = {
        'selected_plan': plan_name,
        'amount': amount,
    }

    if request.method == 'POST':

        bus_pass.payment_status = 'completed'

        bus_pass.final_pass_generated = True

        bus_pass.amount = amount

        # ==========================================
        # NEW APPLICATION
        # ==========================================

        if not bus_pass.renewal_requested:

            bus_pass.start_date = date.today()

            if plan_name == "1 Month":

                bus_pass.end_date = (
                    date.today() + timedelta(days=30)
                )

            elif plan_name == "2 Months":

                bus_pass.end_date = (
                    date.today() + timedelta(days=60)
                )

            elif plan_name == "6 Months":

                bus_pass.end_date = (
                    date.today() + timedelta(days=180)
                )

        # ==========================================
        # RENEWAL FLOW
        # ==========================================

        else:

            if plan_name == "1 Month":

                bus_pass.end_date = (
                    bus_pass.end_date + timedelta(days=30)
                )

            elif plan_name == "2 Months":

                bus_pass.end_date = (
                    bus_pass.end_date + timedelta(days=60)
                )

            elif plan_name == "6 Months":

                bus_pass.end_date = (
                    bus_pass.end_date + timedelta(days=180)
                )

            bus_pass.renewal_requested = False

        bus_pass.save()

        request.session['selected_plan'] = plan_name

        messages.success(
            request,
            "Payment successful. Final E-Pass generated."
        )

        return redirect('final_pass')

    # ==========================================
    # MOBILE / DESKTOP VIEW
    # ==========================================

    if is_mobile(request):

        return render(
            request,
            'payments/mobile_payment.html',
            context
        )

    return render(
        request,
        'payments/desktop_payment.html',
        context
    )


# ==========================================
# FINAL PASS
# ==========================================

@login_required
def final_pass(request):

    bus_pass_id = request.session.get('bus_pass_id')

    if not bus_pass_id:
        return redirect('payment')

    # Secure current user check

    bus_pass = get_object_or_404(
        BusPass,
        id=bus_pass_id,
        student__user=request.user
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


# ==========================================
# MOBILE DETECTION
# ==========================================

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


# ==========================================
# DOWNLOAD PDF PASS
# ==========================================

@login_required
def download_pass(request):

    bus_pass = get_object_or_404(
        BusPass,
        student__user=request.user
    )

    html = render_to_string(

        'payments/final_pass.html',

        {
            'bus_pass': bus_pass,
            'selected_plan': request.session.get(
                'selected_plan'
            )
        }
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="bus_pass.pdf"'

    pisa.CreatePDF(
        html,
        dest=response
    )

    return response