from django.contrib import admin
from employee.models import Role,Department,Employee
# from dashboard.admin import CustomUserAdmins


# admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Role)

admin.site.register(Department)

admin.site.register(Employee)