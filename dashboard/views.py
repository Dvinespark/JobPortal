import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, HttpResponse
from .db_helper import get_rows
from django.http import JsonResponse


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
    return HttpResponse("Create")


def employment_update(request, id):
    return HttpResponse("update")


def employment_delete(request, id):
    return HttpResponse("delete")


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
