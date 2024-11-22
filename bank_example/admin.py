from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Person)
admin.site.register(Bank_account)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Registration)
admin.site.register(FamilyPerson)
