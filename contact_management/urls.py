from django.urls import path
from .views import search, spam

urlpatterns = [
    path("search", search),
    path("spam", spam),
]

