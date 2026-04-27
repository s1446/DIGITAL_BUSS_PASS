from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'phone',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'

        if commit:
            user.save()

        return user