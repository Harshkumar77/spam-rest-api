from django.shortcuts import render
import datetime
from authentication.models import Account, RefreshToken
import json
import bcrypt
import secrets
from django.http import JsonResponse
import re
import jwt
from datetime import datetime, date, timedelta

def register(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        if {"password", "first_name", "last_name", "phone_number"} > body.keys():
            return JsonResponse({"message" : "Incomplete request body"}, status=400)
        if len(body["first_name"]) == 0:
            return JsonResponse({"message" : "First name can't be empty"}, status=406)
        if len(body["password"]) <= 8:
            return JsonResponse({"message" : "Password length should be minimum 8"}, status=406)
        try:
            existingAccount = Account.objects.get(phone_number=body["phone_number"])
            return JsonResponse({"message" : "Phone number is already registered please login"}, status=400)
        except Account.DoesNotExist:
            pass
        hashpw = bcrypt.hashpw(body["password"].encode('utf-8'), bcrypt.gensalt())
        newAccount = Account(first_name=body["first_name"], last_name=body["last_name"], phone_number=body["phone_number"], password=hashpw)
        if "email" in body:
            if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', body["email"]):
                return JsonResponse({"message" : "Invalid email"}, status=406)
            try:
                existingAccount = Account.objects.get(email=body["email"])
                return JsonResponse({"message" : "Email is already registered please login"}, status=400)
            except Account.DoesNotExist:
                pass
            newAccount.email = body["email"]
        newAccount.save()
        return JsonResponse({"message" : "account created"}, status=201)
    return JsonResponse({"message" : "Method not allowed"}, status=405)

def login(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        if {"password", "phone_number"} <= body.keys():
            try:
                account = Account.objects.get(phone_number=body["phone_number"])
                if bcrypt.checkpw(body["password"].encode('utf-8'), account.password):
                    return JsonResponse({"access_token" : getAccessToken(account), "refresh_token" : getRefreshToken(account) }, status=200)
                return JsonResponse({"message" : "Incorrect password"}, status=401)
            except Account.DoesNotExist:
                return JsonResponse({"message" : "account with phone number doesn't exist"}, status=404)
        if {"password", "email"} <= body.keys():
            try:
                account = Account.objects.get(email=body["email"])
                return JsonResponse({"message" : "Email is already registered please login"}, status=400)
                if bcrypt.checkpw(body["password"].encode('utf-8'), account.password):
                    return JsonResponse({"access_token" : getAccessToken(account), "refresh_token" : getRefreshToken(account) }, status=200)
                return JsonResponse({"message" : "Incorrect password"}, status=401)
            except Account.DoesNotExist:
                return JsonResponse({"message" : "account with email doesn't exist"}, status=404)
        JsonResponse({"message" : "Incomplete request body"}, status=400)
    return JsonResponse({"message" : "Method not allowed"}, status=405)

def logout(request):
    if request.method == "POST":
        refresh_token = request.headers["Refresh-Token"]
        try:
            token = RefreshToken.objects.get(token=refresh_token)
            token.delete()
            return JsonResponse({"message" :"Logged out, delete all tokens from client site"}, status=200)
        except Account.DoesNotExist:
            return JsonResponse({"message" : "Logged out already or invalid token"}, status=401)
    return JsonResponse({"message" : "Method not allowed"}, status=405)

def getAccessToken(account):
    return jwt.encode({"id" : account.id, "exp" : datetime.now() + timedelta(minutes=10) }, "secret")

def getRefreshToken(account):
    token = secrets.token_urlsafe(32)
    RefreshToken(token=token, account=account, expiring_at=datetime.now() + timedelta(days=100)).save()
    return token

# print(jwt.decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzEyNDEzMTUyfQ.x-yKLpdkv0s1uHg5uy7o3D5aq5HWDAp70Xn2W5wXCpc", "secret", algorithms="HS256"))

print(RefreshToken.objects.all().values())
print(len(Account.objects.all()))
