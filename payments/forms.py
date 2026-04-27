from django import forms

class ApprovalIDForm(forms.Form):
    approval_id = forms.CharField(
        max_length=50,
        label="Enter Approval ID"
    )