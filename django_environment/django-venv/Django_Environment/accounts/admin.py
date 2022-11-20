from django.contrib import admin

from .models import ETF,ETF_instance

# Register your models here.
admin.site.register(ETF)
admin.site.register(ETF_instance)