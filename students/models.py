# students/models.py

from django.db import models
from accounts.models import CustomUser
import random
from django.core.mail import send_mail
from notifications.models import Notification


# =========================
# Student Profile Model
# =========================

class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    # Personal Details
    full_name = models.CharField(max_length=150)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    aadhaar_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    age = models.IntegerField(
        blank=True,
        null=True
    )

    address = models.TextField()

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    # Travel Details
    route_from = models.CharField(max_length=100)
    route_to = models.CharField(max_length=100)

    # Student Details
    college_name = models.CharField(max_length=200)

    branch = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    year_of_study = models.IntegerField()

    student_id = models.CharField(
        max_length=50,
        unique=True
    )

    # File Uploads
    profile_photo = models.ImageField(
        upload_to='student_profiles/',
        blank=True,
        null=True
    )

    study_certificate = models.FileField(
        upload_to='study_certificates/',
        blank=True,
        null=True
    )

    ssc_certificate = models.FileField(
        upload_to='ssc_certificates/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name


# =========================
# Bus Pass Model
# =========================

class BusPass(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    pass_number = models.CharField(
        max_length=50,
        unique=True
    )

    start_date = models.DateField()
    end_date = models.DateField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    qr_code = models.ImageField(
        upload_to='qr_codes/',
        blank=True,
        null=True
    )

    approval_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=20,
        default='pending'
    )

    final_pass_generated = models.BooleanField(
        default=False
    )

    renewal_requested = models.BooleanField(
        default=False
    )

    pass_pdf = models.FileField(
        upload_to='bus_pass_pdfs/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if self.status == 'approved' and not self.approval_id:
            self.approval_id = "DBP2026" + str(
                random.randint(1000, 9999)
            )

            Notification.objects.create(
                user=self.student.user,
                message=f"Your bus pass has been approved. Approval ID: {self.approval_id}"
            )

            send_mail(
                subject="Bus Pass Approved",
                message=f"""
Your bus pass application has been approved.

Approval ID: {self.approval_id}

Please proceed to payment.
                """,
                from_email=None,
                recipient_list=[self.student.user.email],
                fail_silently=False,
            )

        super().save(*args, **kwargs)

class GovernmentEmployeeProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    # Personal Details
    full_name = models.CharField(max_length=150)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    aadhaar_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    age = models.IntegerField(
        blank=True,
        null=True
    )

    address = models.TextField()

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    # Travel Details
    route_from = models.CharField(max_length=100)
    route_to = models.CharField(max_length=100)

    # Government Employee Details
    department_name = models.CharField(max_length=200)
    employee_id = models.CharField(
        max_length=50,
        unique=True
    )

    pf_number = models.CharField(
        max_length=50,
        unique=True
    )

    office_address = models.TextField()

    # File Uploads
    profile_photo = models.ImageField(
        upload_to='govt_employee_profiles/',
        blank=True,
        null=True
    )

    id_card_upload = models.FileField(
        upload_to='govt_employee_id_cards/',
        blank=True,
        null=True
    )
class NonGovernmentEmployeeProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    # Personal Details
    full_name = models.CharField(max_length=150)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    aadhaar_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    age = models.IntegerField(
        blank=True,
        null=True
    )

    address = models.TextField()

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    # Travel Details
    route_from = models.CharField(max_length=100)
    route_to = models.CharField(max_length=100)

    # Company Details
    company_name = models.CharField(max_length=200)

    employee_id = models.CharField(
        max_length=50,
        unique=True
    )

    work_location = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)

    # File Uploads
    profile_photo = models.ImageField(
        upload_to='private_employee_profiles/',
        blank=True,
        null=True
    )

    salary_slip = models.FileField(
        upload_to='salary_slips/',
        blank=True,
        null=True
    )

class CitizenProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    # Personal Details
    full_name = models.CharField(max_length=150)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    aadhaar_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    age = models.IntegerField(
        blank=True,
        null=True
    )

    address = models.TextField()

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    # Travel Details
    route_from = models.CharField(max_length=100)
    route_to = models.CharField(max_length=100)

    # Citizen Details
    occupation = models.CharField(max_length=150)
    monthly_income = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    purpose_of_travel = models.CharField(max_length=200)

    # File Uploads
    profile_photo = models.ImageField(
        upload_to='citizen_profiles/',
        blank=True,
        null=True
    )

    residence_proof = models.FileField(
        upload_to='residence_proofs/',
        blank=True,
        null=True
    )
class PWDProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    # Personal Details
    full_name = models.CharField(max_length=150)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    aadhaar_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    age = models.IntegerField(
        blank=True,
        null=True
    )

    address = models.TextField()

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    # Travel Details
    route_from = models.CharField(max_length=100)
    route_to = models.CharField(max_length=100)

    # PWD Details
    disability_type = models.CharField(max_length=150)

    disability_percentage = models.IntegerField()

    # File Uploads
    profile_photo = models.ImageField(
        upload_to='pwd_profiles/',
        blank=True,
        null=True
    )

    medical_certificate = models.FileField(
        upload_to='medical_certificates/',
        blank=True,
        null=True
    )

    disability_id_card = models.FileField(
        upload_to='disability_id_cards/',
        blank=True,
        null=True
    )

    

    def __str__(self):
        return self.full_name
   


    