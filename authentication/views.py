from authentication.models import Account, RefreshToken
from contact_management.models import Contact
from datetime import datetime, date, timedelta
from django.http import JsonResponse
import bcrypt
import json
import jwt
import re
import secrets

def register(req):
    if req.method == "POST":
        if {"password", "first_name", "last_name", "phone_number"} > req.parsed_body.keys():
            return JsonResponse({"message" : "Incomplete req req.parsed_body"}, status=400)
        if len(req.parsed_body["first_name"]) == 0:
            return JsonResponse({"message" : "First name can't be empty"}, status=406)
        if len(req.parsed_body["password"]) <= 8:
            return JsonResponse({"message" : "Password length should be minimum 8"}, status=406)
        try:
            existingAccount = Account.objects.get(phone_number=req.parsed_body["phone_number"])
            return JsonResponse({"message" : "Phone number is already registered please login"}, status=400)
        except Account.DoesNotExist:
            pass
        hashpw = bcrypt.hashpw(req.parsed_body["password"].encode('utf-8'), bcrypt.gensalt())
        newAccount = Account(first_name=req.parsed_body["first_name"], last_name=req.parsed_body["last_name"], phone_number=req.parsed_body["phone_number"], password=hashpw)
        newContact = Contact(first_name=req.parsed_body["first_name"], last_name=req.parsed_body["last_name"], phone_number=req.parsed_body["phone_number"])
        newContact.save()
        if "email" in req.parsed_body:
            if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', req.parsed_body["email"]):
                return JsonResponse({"message" : "Invalid email"}, status=406)
            try:
                existingAccount = Account.objects.get(email=req.parsed_body["email"])
                return JsonResponse({"message" : "Email is already registered please login"}, status=400)
            except Account.DoesNotExist:
                pass
            newAccount.email = req.parsed_body["email"]
        newAccount.save()
        return JsonResponse({"message" : "account created"}, status=201)
    return JsonResponse({"message" : "Method not allowed"}, status=405)

def login(req):
    if req.method == "POST":
        if {"password", "phone_number"} <= req.parsed_body.keys():
            try:
                account = Account.objects.get(phone_number=req.parsed_body["phone_number"])
                if bcrypt.checkpw(req.parsed_body["password"].encode('utf-8'), account.password):
                    return JsonResponse({"access_token" : getAccessToken(account), "refresh_token" : getRefreshToken(account) }, status=200)
                return JsonResponse({"message" : "Incorrect password"}, status=401)
            except Account.DoesNotExist:
                return JsonResponse({"message" : "account with phone number doesn't exist"}, status=404)
        if {"password", "email"} <= req.parsed_body.keys():
            try:
                account = Account.objects.get(email=req.parsed_body["email"])
                return JsonResponse({"message" : "Email is already registered please login"}, status=400)
                if bcrypt.checkpw(req.parsed_body["password"].encode('utf-8'), account.password):
                    return JsonResponse({"access_token" : getAccessToken(account), "refresh_token" : getRefreshToken(account) }, status=200)
                return JsonResponse({"message" : "Incorrect password"}, status=401)
            except Account.DoesNotExist:
                return JsonResponse({"message" : "account with email doesn't exist"}, status=404)
        JsonResponse({"message" : "Incomplete req req.parsed_body"}, status=400)
    return JsonResponse({"message" : "Method not allowed"}, status=405)

def logout(req):
    if req.method == "POST":
        if not "Refresh-Token" in req.headers:
            return JsonResponse({"message" : "No Token Provided"}, status=401)
        refresh_token = req.headers["Refresh-Token"]
        try:
            token = RefreshToken.objects.get(token=refresh_token)
            token.delete()
            return JsonResponse({"message" :"Logged out, delete all tokens from client site"}, status=200)
        except RefreshToken.DoesNotExist:
            return JsonResponse({"message" : "Logged out already or invalid token"}, status=401)
    return JsonResponse({"message" : "Method not allowed"}, status=405)

def access_token(req):
    if req.method == "GET":
        if not "Refresh-Token" in req.headers:
            return JsonResponse({"message" : "No Token Provided"}, status=401)
        refresh_token = req.headers["Refresh-Token"]
        try:
            token = RefreshToken.objects.get(token=refresh_token)
            access_token = getAccessToken(token.account)
            return JsonResponse({"access_token" :access_token}, status=200)
        except RefreshToken.DoesNotExist:
            return JsonResponse({"message" : "Logged out already or invalid token"}, status=401)
    return JsonResponse({"message" : "Method not allowed"}, status=405)

def getAccessToken(account):
    return jwt.encode({"id" : account.id, "exp" : datetime.now() + timedelta(minutes=10) }, "secret", algorithm="HS256")

def getRefreshToken(account):
    token = secrets.token_urlsafe(32)
    RefreshToken(token=token, account=account, expiring_at=datetime.now() + timedelta(days=100)).save()
    return token
