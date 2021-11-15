import json
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from dashboard.db_helper import get_rows


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
    results = get_rows(sql)
    context = {
        'data': json.dumps(results, cls=DjangoJSONEncoder)
    }
    return render(request, 'index.html', context=context)
