from django.shortcuts import render, HttpResponse
import datetime
from authentication.models import Account
import json
import bcrypt
from django.http import JsonResponse
import re
import jwt
from datetime import datetime, date, timedelta

def register(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        if {"password", "first_name", "last_name", "phone_number"} > body.keys():
            return HttpResponse(JsonResponse({"message" : "Incomplete request body"}), status=400)
        if len(body["first_name"]) == 0:
            return HttpResponse(JsonResponse({"message" : "First name can't be empty"}), status=406)
        if len(body["password"]) <= 8:
            return HttpResponse(JsonResponse({"message" : "Password length should be minimum 8"}), status=406)
        try:
            existingAccount = Account.objects.get(phone_number=body["phone_number"], registered=True)
            return HttpResponse(JsonResponse({"message" : "Phone number is already registered please login"}), status=400)
        except Account.DoesNotExist:
            pass
        hashpw = bcrypt.hashpw(body["password"].encode('utf-8'), bcrypt.gensalt())
        newAccount = Account(first_name=body["first_name"], last_name=body["last_name"], phone_number=body["phone_number"], password=hashpw, registered=True)
        if "email" in body:
            if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', body["email"]):
                return HttpResponse(JsonResponse({"message" : "Invalid email"}), status=406)
            try:
                existingAccount = Account.objects.get(email=body["email"])
                return HttpResponse(JsonResponse({"message" : "Email is already registered please login"}), status=400)
            except Account.DoesNotExist:
                pass
            newAccount.email = body["email"]
        newAccount.save()
        return HttpResponse(JsonResponse({"message" : "account created"}, status=201))
    return HttpResponse(status=405)

def login(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        if {"password", "phone_number"} <= body.keys():
            try:
                account = Account.objects.get(phone_number=body["phone_number"], registered=True)
                if bcrypt.checkpw(body["password"].encode('utf-8'), account.password):
                    return HttpResponse(JsonResponse({"token" : genToken(account.id)}, status=200))
                return HttpResponse(JsonResponse({"message" : "Incorrect password"}, status=401))
            except Account.DoesNotExist:
                return HttpResponse(JsonResponse({"message" : "account with phone number doesn't exist"}, status=404))
        if {"password", "email"} <= body.keys():
            try:
                account = Account.objects.get(email=body["email"])
                return HttpResponse(JsonResponse({"message" : "Email is already registered please login"}), status=400)
                if bcrypt.checkpw(body["password"].encode('utf-8'), account.password):
                    return HttpResponse(JsonResponse({"token" : genToken(account.id)}, status=200))
                return HttpResponse(JsonResponse({"message" : "Incorrect password"}, status=401))
            except Account.DoesNotExist:
                return HttpResponse(JsonResponse({"message" : "account with email doesn't exist"}, status=404))
        HttpResponse(JsonResponse({"message" : "Incomplete request body"}), status=400)
    return HttpResponse(status=405)

def genToken(id):
    return jwt.encode({"id" : id, "exp" : datetime.now() + timedelta(days=10) }, "secret")
# print(jwt.decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzEyNDEzMTUyfQ.x-yKLpdkv0s1uHg5uy7o3D5aq5HWDAp70Xn2W5wXCpc", "secret", algorithms="HS256"))

print(Account.objects.all().values())
print(len(Account.objects.all()))
