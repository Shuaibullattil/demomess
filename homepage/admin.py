from django.contrib import admin
from .models import Student,MessCut,MessBill,StudentBill

# Register your models here.
admin.site.register(Student)
admin.site.register(MessCut)
admin.site.register(MessBill)
admin.site.register(StudentBill)


