from django import forms
from employee.models import Role,Department,Employee
from django.contrib.auth.models import User
from .models import User

from django import forms

# class EmployeeCreateForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'email', 'password', 'username',)
        
     
#     def clean(self):
#         cleaned_data = super(EmployeeCreateForm, self).clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
        
#         if password != confirm_password:   
#             raise forms.ValidationError(
#                 "Passwords do not match"
#             )

# EMPLoYEE
class EmployeeCreateForm(forms.ModelForm):
	employeeid = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'please enter 5 characters without RGL or slashes eg. A0025'}))
	image = forms.ImageField(widget=forms.FileInput(attrs={'onchange':'previewImage(this);'}))
	class Meta:
		model = Employee
		exclude = ['is_blocked','is_deleted','created','updated']
		widgets = {
				'bio':forms.Textarea(attrs={'cols':5,'rows':5})
		}

