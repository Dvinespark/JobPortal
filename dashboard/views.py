import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, HttpResponse, redirect
from .db_helper import get_rows
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import EmploymentForm, SeekerForm
from .models import Employer, Employees


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name="SecondAdmin").exists():
            return render(request, 'dashboard.html', context={})
        else:
            return redirect('webapp:home')
    return redirect('webapp:login')


# ----------------Employment------------------
def employment_list(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name="SecondAdmin").exists():
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
                from Employer
            """

            if request.user.groups.filter(name="SecondAdmin"):
                sql += "where created_by = '" + request.user.username + "'"
            results = get_rows(sql)
            context = {
                'data': json.dumps(results, cls=DjangoJSONEncoder),
                'page_title': "Employments"
            }
            return render(request, 'employments.html', context=context)
        return redirect('webapp:home')
    return redirect('webapp:login')


def employment_create(request):
    # TODO Error handling and optimization required
    if request.method == "GET":
        form = EmploymentForm()
        return render(request, 'employment_create.html', context={"form": form, "page_title": "Employment"})
    if request.method == "POST":
        form = EmploymentForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = request.user.username
            data.updated_by = None
            data.save()
        return redirect("dashboard:employment_list")


def employment_update(request, job_id):
    if request.method == "GET":
        form = EmploymentForm(instance=Employer.objects.get(id=job_id))
        context_data = {
            'form': form,
            'job_id': job_id,
            'page_title': "Employment"
        }
        return render(request, "employment_update.html", context=context_data)
    if request.method == "POST":
        instance = Employer.objects.get(id=job_id)
        form = EmploymentForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updated_by = request.user.username
            data.save()
        return redirect("dashboard:employment_list")


def employment_delete(request, job_id):
    instance = Employer.objects.get(id=job_id)
    instance.delete()
    return redirect("dashboard:employment_list")


# ----------------End of Employment------------------


# ----------------Employees------------------
def job_seeker_list(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name="SecondAdmin").exists():
            sql = """
                SELECT s.id,
                    s.firstname,
                    s.lastname,
                    s.email,
                    s.skill,
                    s.experience_year,
                    s.phone_number,
                    s.status,
                    s.availability,
                    s.resume,
                    s.employer_id
                FROM
                Employees as s
            """
            sql += "inner join Employer e " \
                   "on s.employer_id = e.id where e.created_by = '" + request.user.username + "'"
            results = get_rows(sql)
            data = json.dumps(results, cls=DjangoJSONEncoder)
            context = {
                'data': data,
                'page_title': "Candidates"
            }
            print(context['data'])
            return render(request, 'jobseekers.html', context=context)
        else:
            return redirect('webapp:home')
    return redirect('webapp:login')


def seeker_create(request):
    if request.method == "GET":
        form = SeekerForm()
        return render(request, 'seeker_create.html', context={"form": form, "page_title": "Candidate"})
    if request.method == "POST":
        form = SeekerForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = request.user.username
            data.updated_by = None
            data.save()
        return redirect("dashboard:job_seeker_list")


def seeker_update(request, seeker_id):
    if request.method == "GET":
        form = SeekerForm(instance=Employees.objects.get(id=seeker_id))
        context_data = {
            'form': form,
            'seeker_id': seeker_id,
            'page_title': "Candidate"
        }
        return render(request, "seeker_update.html", context=context_data)
    if request.method == "POST":
        instance = Employees.objects.get(id=seeker_id)
        form = SeekerForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updated_by = request.user.username
            data.save()
        return redirect("dashboard:job_seeker_list")


def seeker_delete(request, seeker_id):
    instance = Employees.objects.get(id=seeker_id)
    instance.delete()
    return redirect("dashboard:job_seeker_list")


# ----------------End of Employees------------------
def seekers_filter(request):
    # check if request params exists
    skills = request.GET.get('skills', '')
    years = request.GET.get('years', '')
    lastname = request.GET.get('lastname', '')
    query = """
        SELECT s.id,
            s.firstname,
            s.lastname,
            s.email,
            s.skill,
            s.experience_year,
            s.phone_number,
            s.status,
            s.availability,
            s.resume,
            s.employer_id
        FROM
        Employees s
        inner join Employer e
        on s.employer_id = e.id and e.created_by = '{0}'
        WHERE lower(skill) like '%{1}%' and experience_year like '%{2}%' and lower(lastname) like '%{3}%'; """\
        .format(request.user.username, skills.lower() if skills else '', years if years else '', lastname.lower() if lastname else '')
    results = get_rows(sql=query)
    data = json.dumps(results, cls=DjangoJSONEncoder)
    return JsonResponse({"status": 200, "data": data})
