import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, HttpResponse, redirect
from .db_helper import get_rows
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import EmploymentForm
from .models import Employer


# Create your views here.
def index(request):
    return render(request, 'dashboard.html', context={})


# ----------------Employment------------------
def employment_list(request):
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
    context = {
        'data': json.dumps(results, cls=DjangoJSONEncoder)
    }
    print(context['data'])
    return render(request, 'employments.html', context=context)


def employment_create(request):
    # TODO Error handling and optimization required

    if request.method == "POST":
        form_data = {
            "job_title": request.POST.get('job_title', ''),
            "company": request.POST.get('company', ''),
            "email": request.POST.get('email', ''),
            "job_description": request.POST.get('job_description', None),
            "rate": request.POST.get("rate", None),
            "availability": request.POST.get("availability", None),
            "duration": request.POST.get("duration", None),
            "employment_type": request.POST.get("employment_type", None),
            "status": True,
            "created_by": request.user.username,
            "updated_by": None

        }
        form = EmploymentForm(form_data, request.FILES)
        if form.is_valid():
            form.save()
        return JsonResponse({
            "status_code": 200,
            "message": "job applied successfully.",
            "url": reverse_lazy('dashboard:employment_list')
        })
    return redirect("dashboard:employment_list")


def employment_update(request, job_id):
    if request.method == "GET":
        form = EmploymentForm(instance=Employer.objects.get(id=job_id))
        context_data = {
            'employment_form': form
        }
        return render(request, "index.html", context= context_data)
    if request.method == "POST":
        instance = Employer.objects.get(id=job_id)

        form_data = {
            "job_title": request.POST.get('job_title', ''),
            "company": request.POST.get('company', ''),
            "email": request.POST.get('email', ''),
            "job_description": request.POST.get('job_description', None),
            "rate": request.POST.get("rate", None),
            "availability": request.POST.get("availability", None),
            "duration": request.POST.get("duration", None),
            "employment_type": request.POST.get("employment_type", None),
            "status": request.POST.get('status', True),
            "created_by": instance.created_by,
            "updated_by": request.user.username

        }
        form = EmploymentForm(form_data, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
        return JsonResponse({
            "status_code": 200,
            "message": "job applied successfully.",
            "url": reverse_lazy('dashboard:employment_list')
        })


def employment_delete(request, job_id):
    instance = Employer.objects.get(id=job_id)
    instance.delete()
    return JsonResponse({
        "status_code": 200,
        "message": "Record deleted successfully.",
        "url": reverse_lazy('dashboard:employment_list')
    })


# ----------------End of Employment------------------


# ----------------Employees------------------
def job_seeker_list(request):
    sql = """
        SELECT id,
            firstname,
            lastname,
            email,
            skill,
            experience_year,
            phone_number,
            status,
            availability,
            resume,
            employer_id
        FROM
        employees;
    """

    results = get_rows(sql)
    data = json.dumps(results, cls=DjangoJSONEncoder)
    context = {
        'data': data
    }
    print(context['data'])
    return render(request, 'jobseekers.html', context=context)


def job_seeker_create(request):
    return HttpResponse("Create")


def job_seeker_update(request, id):
    return HttpResponse("update")


def job_seeker_delete(request, id):
    return HttpResponse("delete")


# ----------------End of Employees------------------
def seekers_filter(request):
    # check if request params exists
    skills = request.GET.get('skills', '')
    years = request.GET.get('years', '')
    lastname = request.GET.get('lastname', '')
    query = """
        SELECT id,
            firstname,
            lastname,
            email,
            skill,
            experience_year,
            phone_number,
            status,
            availability,
            resume,
            employer_id
        FROM
        employees
        WHERE lower(skill) like '%{0}%' and experience_year like '%{1}%' and lower(lastname) like '%{2}%'; """\
        .format(skills.lower() if skills else '', years if years else '', lastname.lower() if lastname else '')
    results = get_rows(sql=query)
    data = json.dumps(results, cls=DjangoJSONEncoder)
    return JsonResponse({"status": 200, "data": data})
