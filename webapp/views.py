import json

from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from dashboard.db_helper import get_rows
from forms import UserRegisterForm
from django.contrib import messages


# Create your views here.
def home(request):
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
    # for user login and register
    register_form = UserRegisterForm()
    login_form = AuthenticationForm()
    results = get_rows(sql)
    context = {
        'data': json.dumps(results, cls=DjangoJSONEncoder),
        'register_form': register_form,
        'login_form': login_form
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


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("dashboard:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    return redirect("webapp:home")


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("webapp:home")