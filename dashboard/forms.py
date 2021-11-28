from django import forms
from .models import Employer, Employees


class EmploymentForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['job_title', 'company', 'logo', 'job_description', 'email', 'rate', 'availability', 'duration',
                  'employment_type', 'status', 'created_by', 'updated_by']
        widgets = {
            'created_by': forms.HiddenInput(),
            'updated_by': forms.HiddenInput(),
        }


class SeekerForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['employer', 'firstname', 'lastname', 'email', 'skill', 'experience_year', 'phone_number', 'status',
                  'availability', 'resume', 'created_by', 'updated_by']
        widgets = {
            'created_by': forms.HiddenInput(),
            'updated_by': forms.HiddenInput(),
        }
