from django.contrib import admin
from .models import StudentProfile, BusPass
import random


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'student_id',
        'college_name',
        'branch',
        'year_of_study',
        'phone_number',
        'route_from',
        'route_to',
    )

    search_fields = (
        'full_name',
        'student_id',
        'college_name',
        'aadhaar_number',
        'phone_number',
    )


@admin.register(BusPass)
class BusPassAdmin(admin.ModelAdmin):
    list_display = (
        'pass_number',
        'student',
        'status',
        'approval_id',
        'payment_status',
        'final_pass_generated',
        'start_date',
        'end_date',
        'amount',
    )

    list_filter = (
        'status',
        'payment_status',
    )

    search_fields = (
        'pass_number',
        'approval_id',
    )

    actions = ['approve_selected_applications']

    def approve_selected_applications(self, request, queryset):
        from notifications.models import Notification

        for bus_pass in queryset:

            if bus_pass.status == 'pending':

                bus_pass.status = 'approved'

                if not bus_pass.approval_id:
                    bus_pass.approval_id = "APR" + str(
                        random.randint(10000, 99999)
                    )

                bus_pass.save()

                Notification.objects.create(
                    user=bus_pass.student.user,
                    message=(
                        f"Your bus pass application has been approved. "
                        f"Approval ID: {bus_pass.approval_id}. "
                        f"Please proceed to payment."
                    )
                )

        self.message_user(
            request,
            "Selected applications approved successfully."
        )

    approve_selected_applications.short_description = (
        "Approve selected applications"
    )