from django.contrib import admin
from .models import Leave, CarriedForward
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
# from .models import Comment


admin.site.register(Leave)
admin.site.register(CarriedForward)
# admin.site.unregister(User)
# admin.site.unregister(Group)
# admin.site.register(Comment)
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     def get_form(self, request, obj=None, **kwargs):
#         form=super().get_form(request, obj, **kwargs)
#         is_superuser=request.user.is_superuser
#         is_staff=request.user.is_staff
        
#         if is_staff:
#             form.base_fields['username'].disabled = True
#             form.base_fields['is_superuser'].disabled = True
#             form.base_fields['user_permissions'].disabled = True
#             # form.base_fields['groups'].disabled = False
# return form