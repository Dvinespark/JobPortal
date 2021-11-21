from django.urls import path
from .views import *
app_name = "webapp"
urlpatterns = [
    path('', home, name="home"),
    path('login', login_request, name="login"),
    path('logout', logout_request, name="logout"),
]