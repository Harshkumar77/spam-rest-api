from django.contrib import admin
from .models import Account, RefreshToken

admin.site.register(Account)
admin.site.register(RefreshToken)
