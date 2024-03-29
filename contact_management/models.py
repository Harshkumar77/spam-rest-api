from django.db import models
from authentication.models import Account

class Contact(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=13)
    added_by = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SpamReport(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
