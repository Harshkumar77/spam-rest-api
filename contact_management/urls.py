from django.urls import path
from .views import search, spam, phone_number, view_email

urlpatterns = [
    path("search", search),
    path("spam", spam),
    path("phone-number/<str:phone_number>", phone_number),
    path("view-email/<str:phone_number>", view_email),
]

