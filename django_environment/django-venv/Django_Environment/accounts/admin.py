from django.contrib import admin

from .models import ETF,ETF_instance, Code, CustomUser

# Register your models here.
admin.site.register(ETF)
admin.site.register(ETF_instance)

admin.site.register(Code)
admin.site.register(CustomUser)