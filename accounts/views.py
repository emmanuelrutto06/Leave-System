from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from employee.models import *
from .forms import UserLogin, UserAddForm

def changepassword(request):
	if not request.user.is_authenticated:
		return redirect('/')
	'''
	Please work on me -> success & error messages & style templates
	'''
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save(commit=True)
			update_session_auth_hash(request,user)

			messages.success(request,'Password changed successfully',extra_tags = 'alert alert-success alert-dismissible show' )
			# return redirect('accounts:changepassword')
		else:
			messages.error(request,'Error,changing password',extra_tags = 'alert alert-warning alert-dismissible show' )
			return redirect('accounts:changepassword')
			
	form = PasswordChangeForm(request.user)
	return render(request,'accounts/change_password_form.html',{'form':form})




def register_user_view(request):
	# I NEED TO WORK ON (MESSAGES AND UI) & extend with email field
	if request.method == 'POST':
		form = UserAddForm(data = request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			instance.save()
			email = form.cleaned_data.get("email") #changed username to email

			messages.success(request,'Account created for {0} !!!'.format(email),extra_tags = 'alert alert-success alert-dismissible show' )
			return redirect('accounts:register')
		else:
			messages.error(request,'The Email or password is invalid',extra_tags = 'alert alert-warning alert-dismissible show')
			return redirect('accounts:register')


	form = UserAddForm()
	dataset = dict()
	dataset['form'] = form
	dataset['title'] = 'register users'
	return render(request,'accounts/register.html',dataset)



# def login_view(request):
#     if request.method == 'POST':
#         form = UserLogin(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')

#             user = authenticate(request, username=username, password=password)
#             if user is not None and user.is_active:
#                 login(request, user)
#                 return redirect('dashboard:dashboard')
#             else:
#                 messages.error(request, 'Invalid username or password', extra_tags='alert alert-error alert-dismissible show')
#                 return redirect('accounts:login')
#         else:
#             messages.error(request, 'Invalid form data', extra_tags='alert alert-error alert-dismissible show')
#             return redirect('accounts:login')
#     else:
#         form = UserLogin()

#     dataset = {'form': form}
#     return render(request, 'accounts/login.html', dataset)

def login_view(request):
	'''
	I need to work on needs messages and redirects
	
	'''
	# login_user = request.user
	if request.method == 'POST':
		form = UserLogin(data = request.POST)
		if form.is_valid():
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username = username, password = password)
			if user and user.is_active:
				login(request,user)
				if user.is_authenticated:
					return redirect('dashboard:dashboard')
			else:
				messages.error(request,'Account is invalid',extra_tags = 'alert alert-error alert-dismissible show' )
				return redirect('accounts:login')

		else:
			return HttpResponse('data not valid')

	dataset=dict()
	form = UserLogin()

	dataset['form'] = form
	return render(request,'accounts/login.html',dataset)




# def user_profile_view(request):
# 	'''
# 	user profile view -> staffs (No edit) only admin/HR can edit.
# 	'''
# 	user = request.user
# 	if user.is_authenticated:
# 		employee = Employee.objects.filter(user = user).first()
		

# 		dataset = dict()
# 		dataset['employee'] = employee
	
		

# 		return render(request,'dashboard/employee_detail.html',dataset)
# 	return HttpResponse("Sorry , not authenticated for this,admin or whoever you are :)")





def logout_view(request):
	logout(request)
	return redirect('accounts:login')



def users_list(request):
	employees = Employee.objects.all()
	return render(request,'accounts/users_table.html',{'employees':employees,'title':'Users List'})


def users_unblock(request,id):
	user = get_object_or_404(CustomUser,id = id)#modified customuser
	emp = Employee.objects.filter(user = user).first()
	emp.is_blocked = False
	emp.save()
	user.is_active = True
	user.save()

	return redirect('accounts:users')


def users_block(request,id):
	user = get_object_or_404(CustomUser,id = id)#customuser edited
	emp = Employee.objects.filter(user = user).first()
	emp.is_blocked = True
	emp.save()
	
	user.is_active = False
	user.save()
	
	return redirect('accounts:users')



def users_blocked_list(request):
	blocked_employees = Employee.objects.all_blocked_employees()
	return render(request,'accounts/all_deleted_users.html',{'employees':blocked_employees,'title':'blocked users list'})