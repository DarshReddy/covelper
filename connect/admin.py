from django.contrib import admin
from .models import MyUser,Patient,HealthWorker,Request

admin.site.register(MyUser)
admin.site.register(Patient)
admin.site.register(HealthWorker)
admin.site.register(Request)