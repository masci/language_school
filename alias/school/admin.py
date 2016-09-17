from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import *


class SchoolAdminSite(AdminSite):
    site_header = 'Monty Python administration'
admin_site = SchoolAdminSite(name='myadmin')

admin_site.register(Person)
admin_site.register(Partner)
admin_site.register(Lodge)
admin_site.register(Student)
admin_site.register(CourseLevel)
admin_site.register(Session)
admin_site.register(CostItem)
admin_site.register(Course)
admin_site.register(Staying)
