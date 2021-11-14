from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('employments', employment_list, name='employment_list'),
    path('jobseeker', job_seeker_list, name='job_seeker_list')
]