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

from django import forms
from .models import Family

class FamilyCreateForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['status', 'spouse', 'occupation', 'tel', 'children', 'nextofkin', 'contact', 'relationship', 'father', 'foccupation', 'mother', 'moccupation']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'spouse': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control'}),
            'children': forms.NumberInput(attrs={'class': 'form-control'}),
            'nextofkin': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'father': forms.TextInput(attrs={'class': 'form-control'}),
            'foccupation': forms.TextInput(attrs={'class': 'form-control'}),
            'mother': forms.TextInput(attrs={'class': 'form-control'}),
            'moccupation': forms.TextInput(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import Emergency

class EmergencyCreateForm(forms.ModelForm):
    class Meta:
        model = Emergency
        fields = ['fullname', 'tel', 'location', 'relationship']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import Bank

class BankCreateForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'account', 'branch', 'salary']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
        }
