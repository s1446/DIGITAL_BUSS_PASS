from django import forms
from .models import StudentProfile
from .models import GovernmentEmployeeProfile
from .models import NonGovernmentEmployeeProfile
from .models import CitizenProfile
from .models import PWDProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'full_name',
            'phone_number',
            'aadhaar_number',
            'gender',
            'age',
            'address',
            'postal_code',
            'route_from',
            'route_to',
            'college_name',
            'branch',
            'year_of_study',
            'student_id',
            'profile_photo',
            'study_certificate',
            'ssc_certificate',
        ]

class GovernmentEmployeeForm(forms.ModelForm):
    class Meta:
        model = GovernmentEmployeeProfile
        exclude = ['user']

class NonGovernmentEmployeeForm(forms.ModelForm):
    class Meta:
        model = NonGovernmentEmployeeProfile
        exclude = ['user']

class CitizenForm(forms.ModelForm):
    class Meta:
        model = CitizenProfile
        exclude = ['user']


class PWDForm(forms.ModelForm):
    class Meta:
        model = PWDProfile
        exclude = ['user']