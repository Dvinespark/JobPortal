from django.urls import path
from .views import *
app_name = "webapp"
urlpatterns = [
    path('', home, name="home"),
]