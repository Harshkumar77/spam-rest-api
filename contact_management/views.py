import datetime
import jwt
import json
from contact_management.models import SpamReport, Contact
from authentication.models import Account
from django.http import JsonResponse
from django.db.models import Q

def spam(req):
    if req.method == "POST":
        if not 'phone_number' in req.parsed_body:
            return JsonResponse({"message" : "Phone number is required"}, status=400)
        contact, created = Contact.objects.get_or_create(
            phone_number=req.parsed_body["phone_number"]
        )
        report = SpamReport(
            contact=contact,
            reported_by=req.account,
        )
        report.save()
        return JsonResponse({"message" : "Number Flagged as spam"}, status=201)
    return JsonResponse({"message" : "Method not allowed"}, status=405)

def search(req):
    if req.method == "GET":
        if req.GET.get("q") != None:
            query = req.GET.get("q")
            search_filter = Contact.objects.filter(first_name__startswith=query) | Contact.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
            search_results = search_filter.values()
            return JsonResponse({"contacts" : list(search_results)}, safe=False, status=200)
        return JsonResponse({"message" : "Search query is required"}, status=400)
    return JsonResponse({"message" : "Method not allowed"}, status=405)

def phone_number(req, phone_number):
    if req.method == "GET":
        contacts = Contact.objects.filter(phone_number=phone_number).values()
        return JsonResponse({"contacts_with_given_phone_number" : list(contacts)}, safe=False, status=200)
    return JsonResponse({"message" : "Method not allowed"}, status=405)

def view_email(req, phone_number):
    if req.method == "GET":
        try:
            account = Account.objects.get(phone_number=phone_number)
        except Account.DoesNotExist:
            return JsonResponse({"message" : "we don't have email"}, status=200)
        try:
            contact = Contact.objects.get(phone_number=phone_number, added_by=account)
        except Contact.DoesNotExist:
            return JsonResponse({"message" : "Contacts are not mutual"}, status=400)
        if account.email == None:
            return JsonResponse({"message" : "Contacts are mutual but we don't have email"}, status=200)
        return JsonResponse({"email" : account.email}, status=200)
    return JsonResponse({"message" : "Method not allowed"}, status=405)
