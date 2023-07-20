from django import forms
from employee.models import User
from django.contrib.auth.forms import UserCreationForm

class UserAddForm(UserCreationForm):
    '''
    Extending UserCreationForm - with email
    '''
    
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'username'}))

    class Meta:
        model = User  # Use the CustomUser model instead of User
        fields = ['email', 'username', 'password1', 'password2']






# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm




# class UserAddForm(UserCreationForm):
# 	'''
# 	Extending UserCreationForm - with email

# 	'''
# 	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'eg.emmanuelrutto@gmail.com'}))

# 	# The class Meta defines the model and fields for a User form.
# 	class Meta:
# 		model = User
# 		fields = ['username','email','password1','password2']
  
		

	





class UserLogin(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))



