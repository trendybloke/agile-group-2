from django.contrib import admin

from .models import ETF,ETF_instance,User_Details,Account,Transaction_Type,Transaction

# Register your models here.
admin.site.register(ETF)
admin.site.register(ETF_instance)
admin.site.register(User_Details)
admin.site.register(Account)
admin.site.register(Transaction_Type)
admin.site.register(Transaction)