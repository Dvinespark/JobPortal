from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from dashboard.models import Employees
import datetime


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class JobApplyForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['employer', 'firstname', 'lastname', 'email', 'phone_number', 'status', 'availability', 'resume', 'skill', 'experience_year']