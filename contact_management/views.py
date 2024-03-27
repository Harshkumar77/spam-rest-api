from django.shortcuts import render, HttpResponse
import datetime

# Create your views here.

def spam(request):
    current_time = datetime.datetime.utcnow()
    return HttpResponse(f"Test Response current time is {current_time}")

def search(request):
    current_time = datetime.datetime.utcnow()
    return HttpResponse(f"Test Response current time is {current_time}")
