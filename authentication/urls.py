from django.urls import path
from .views import login, register, logout, access_token

urlpatterns = [
    path("login", login),
    path("register", register),
    path("logout", logout),
    path("access_token", access_token),
]

