from django.urls import path
from .views import *

app_name = "dashboard"
urlpatterns = [
    path('', index, name="index"),
    path('employments', employment_list, name='employment_list'),
    path('jobseeker', job_seeker_list, name='job_seeker_list'),
    path('jobseeker/filter', seekers_filter, name='seeker_filter')
]