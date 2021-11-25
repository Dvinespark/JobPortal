import json
import datetime
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from dashboard.models import Employer
from django.urls import reverse_lazy
from dashboard.db_helper import get_rows
from .forms import UserRegisterForm, JobApplyForm
from django.contrib import messages
from django.http import JsonResponse


def home_data():
    sql = """
        SELECT id, 
            job_title,
            company,
            logo,
            job_description,
            email,
            rate,
            availability,
            duration,
            employment_type,
            status,
            date(created_at) as created_at
        from employer;
    """
    results = get_rows(sql)
    return json.dumps(results, cls=DjangoJSONEncoder)


# Create your views here.
def home(request):
    # for user login and register
    register_form = UserRegisterForm()
    login_form = AuthenticationForm()
    job_form = JobApplyForm()
    context = {
        'data': home_data(),
        'register_form': register_form,
        'login_form': login_form,
        'job_form': job_form
    }
    return render(request, 'index.html', context=context)


# login / register /logout view
def register_request(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("dashboard:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return redirect("webapp:home")


def login_request(request):
    print("function triggered")
    if request.method == "POST":
        print(request.POST)
        form = AuthenticationForm(request, data=request.POST or None)
        print(form)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            print(password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("dashboard:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            register_form = UserRegisterForm()
            login_form = form
            context = {
                'data': home_data(),
                'register_form': register_form,
                'login_form': login_form
            }
            return render(request, 'index.html', context=context)
    return redirect("webapp:home")


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('webapp:home')


def apply_job(request):
    # TODO Error handling and optimization required

    if request.method == "POST":
        skill1 = request.POST.get("skill1", None)
        nskill1 = request.POST.get("nskill1", None)
        skill2 = request.POST.get("skill2", None)
        nskill2 = request.POST.get("nskill2", None)
        skill3 = request.POST.get("skill3", None)
        nskill3 = request.POST.get("nskill3", None)
        job_id = int(request.POST.get("job_id", None))
        form_data = {
            "employer": Employer.objects.get(id=int(job_id)),
            "firstname": request.POST.get('firstname', ''),
            "lastname": request.POST.get('lastname', ''),
            "email": request.POST.get('email', ''),
            "phone_number": request.POST.get('phone_number', None),
            "status": request.POST.get("status", None),
            "availability": request.POST.get("availability", None)

        }
        skills = [skill1, skill2, skill3]
        years_skills = [nskill1, nskill2, nskill3]
        for skill, years in zip(skills, years_skills):
            if skill is not None:
                form_data['skill'] = skill
                form_data['experience_year'] = years
                form = JobApplyForm(form_data, request.FILES)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.employer = Employer.objects.get(id=job_id)
                    data.save()
        # if skill1 is not None:
        #     form_data['skill'] = skill1
        #     form_data['experience_year'] = nskill1
        #     form = JobApplyForm(form_data, request.FILES)
        #     if form.is_valid():
        #         data = form.save(commit=False)
        #         data.employer = Employer.objects.get(id=1)
        #         data.save()

        # if skill2 is not None:
        #     form_data['skill'] = skill2
        #     form_data['experience_year'] = nskill2
        #     form = JobApplyForm(form_data, request.FILES)
        #     if form.is_valid():
        #         data = form.save(commit=False)
        #         data.employer = Employer.objects.get(id=1)
        #         data.save()
        #
        # if skill3 is not None:
        #     form_data['skill'] = skill3
        #     form_data['experience_year'] = nskill3
        #     form = JobApplyForm(form_data, request.FILES)
        #     if form.is_valid():
        #         data = form.save(commit=False)
        #         data.employer = Employer.objects.get(id=1)
        #         data.save()
        return JsonResponse({
            "status_code": 200,
            "message": "job applied successfully.",
            "url": reverse_lazy('webapp:home')
        })
    return redirect("webapp:home")
