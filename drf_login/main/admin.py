from django.contrib import admin
from main.models import Good, Check, Transaction, userProfile
# Register your models here.
admin.site.register(Good)
admin.site.register(Check)
admin.site.register(Transaction)
admin.site.register(userProfile)