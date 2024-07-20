from django.contrib import admin
from employee.models import Role,Department,Employee, Family, Bank, Emergency
# from dashboard.admin import CustomUserAdmins


# admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Role)

admin.site.register(Department)

admin.site.register(Employee)
admin.site.register(Family)
admin.site.register(Emergency)
admin.site.register(Bank)