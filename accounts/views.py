from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import CarriedForwardForm
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

from .forms import CarriedForwardForm
from datetime import date, timedelta
from django.conf import settings
from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect
from leave.models import CarriedForward
from .models import FinancialYear


def register_user_view(request):
    if request.method == 'POST':
        form = UserAddForm(data=request.POST)
        carried_forward_form = CarriedForwardForm(request.POST)
        
        if form.is_valid() and carried_forward_form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            email = form.cleaned_data.get("email")
            
            # Check if the user is a staff member
            if request.user.is_staff:
                carried_forward_days = carried_forward_form.cleaned_data['carried_forward_days']
                carried_forward_days = min(carried_forward_days, 15)  # Limit carried forward days to 15
                
                financial_year, created = FinancialYear.objects.get_or_create(
                    start_date=date.today().replace(month=7, day=1),
                    end_date=(date.today().replace(month=6, day=30) + timedelta(days=1))
                )
                
                carried_forward, created = CarriedForward.objects.get_or_create(
                    user=instance,
                    financial_year=financial_year,
                    defaults={'leave_days_carried_forward': carried_forward_days}
                )
                if not created:
                    carried_forward.leave_days_carried_forward = carried_forward_days
                    carried_forward.save()
                
                messages.success(request, f'Account created for {email}!')
            else:
                messages.error(request, 'You do not have permission to perform this action.')
                
            dataset = {
                'form': form,
                'carried_forward_form': carried_forward_form,
                'title': 'register users',
            }
            return render(request, 'accounts/register.html', dataset)
        else:
            messages.error(request, 'Invalid input. Please check your information.')
            return redirect('accounts:register')

    form = UserAddForm()
    carried_forward_form = CarriedForwardForm()
    dataset = {
        'form': form,
        'carried_forward_form': carried_forward_form,
        'title': 'register users'
    }
    return render(request, 'accounts/register.html', dataset)

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




def user_profile_view(request):
	'''
	user profile view -> staffs (No edit) only admin/HR can edit.
	'''
	user = request.user
	if user.is_authenticated:
		employee = Employee.objects.filter(user = user).first()
		

		dataset = dict()
		dataset['employee'] = employee
	
		

		return render(request,'dashboard/employee_detail.html',dataset)
	return HttpResponse("Sorry , not authenticated for this,admin or whoever you are :)")


def logout_view(request):
	logout(request)
	return redirect('accounts:login')

def users_list(request):
	employees = Employee.objects.all()
	return render(request,'accounts/users_table.html',{'employees':employees,'title':'Users List'})


def users_unblock(request,id):
	user = get_object_or_404(User,id = id)
	emp = Employee.objects.filter(user = user).first()
	emp.is_blocked = False
	emp.save()
	user.is_active = True
	user.save()

	return redirect('accounts:users')


def users_block(request,id):
	user = get_object_or_404(User,id = id)#customuser edited
	emp = Employee.objects.filter(user = user).first()
	emp.is_blocked = True
	emp.save()
	
	user.is_active = False
	user.save()
	
	return redirect('accounts:users')



def users_blocked_list(request):
	blocked_employees = Employee.objects.all_blocked_employees()
	return render(request,'accounts/all_deleted_users.html',{'employees':blocked_employees,'title':'blocked users list'})