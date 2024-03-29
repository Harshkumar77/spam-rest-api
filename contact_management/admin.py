from django.contrib import admin
from .models import SpamReport, Contact

admin.site.register(SpamReport)
admin.site.register(Contact)
