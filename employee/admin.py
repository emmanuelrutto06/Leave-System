from django.contrib import admin
from employee.models import Role,Department,Employee, Family, Bank, Emergency
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
admin.site.register(Role)

admin.site.register(Department)

admin.site.register(Employee)
admin.site.register(Family)
admin.site.register(Emergency)
admin.site.register(Bank)




class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    filter_horizontal = []  # Remove default filters

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
