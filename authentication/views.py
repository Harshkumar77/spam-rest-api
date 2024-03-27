from django.shortcuts import render, HttpResponse
import datetime

def register(request):
    current_time = datetime.datetime.utcnow()
    return HttpResponse(f"Test Response current time is {current_time}")

def login(request):
    current_time = datetime.datetime.utcnow()
    return HttpResponse(f"Test Response current time is {current_time}")
