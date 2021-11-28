from django.urls import path
from .views import *

app_name = "dashboard"
urlpatterns = [
    path('', index, name="index"),
    path('employments', employment_list, name='employment_list'),
    path('jobseeker', job_seeker_list, name='job_seeker_list'),
    path('jobseeker/filter', seekers_filter, name='seeker_filter'),

    # employment
    path('employment/create', employment_create, name='employment_create'),
    path('employment/update/<int:job_id>', employment_update, name='employment_update'),
    path('employment/delete/<int:job_id>', employment_delete, name='employment_delete'),

    # seekers
    path('seeker/create', seeker_create, name='seeker_create'),
    path('seeker/update/<int:seeker_id>', seeker_update, name='seeker_update'),
    path('seeker/delete/<int:seeker_id>', seeker_delete, name='seeker_delete'),

]