from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
import datetime
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from employee.forms import EmployeeCreateForm
from leave.models import Leave
from employee.models import *
from leave.forms import LeaveCreationForm
from datetime import date


def dashboard(request):
    dataset = dict()
    user = request.user
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    employees = Employee.objects.all()
    leaves = Leave.objects.all_pending_leaves()
    leavey = Leave.objects.all_recommended_leaves()
    staff_leaves = Leave.objects.filter(user=user)
    dataset['employees'] = employees
    dataset['leaves'] = leaves
    dataset['leavey'] = leavey
    dataset['staff_leaves'] = staff_leaves
    dataset['title'] = 'summary'

    return render(request, 'dashboard/dashboard_index.html', dataset)


from django.shortcuts import render


def dashboard_employees(request):
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
        return redirect('/')

    dataset = dict()
    departments = Department.objects.all()
    employees = Employee.objects.all()
    dashboard_family = Family.objects.all()

    # Pagination
    query = request.GET.get('search')
    if query:
        employees = employees.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query)
        )

    paginator = Paginator(employees, 10)  # Show 10 employee lists per page
    page = request.GET.get('page')
    employees_paginated = paginator.get_page(page)

    # Include employees in the dataset
    # dataset['employees'] = employees_paginated
    dataset['employees'] = employees
    dataset['dashboard_family'] = dashboard_family

    blocked_employees = Employee.objects.all_blocked_employees()

    return render(request, 'dashboard/employee_app.html', dataset)


from django.shortcuts import render, redirect
from django.contrib import messages


# from .forms import EmployeeCreateForm
# from .models import Employee, Role, Department
# from django.contrib.auth.models import User

# def dashboard_employees_create(request):
#     if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
#         return redirect('/')
#
#     if request.method == 'POST':
#         form = EmployeeCreateForm(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#
#             # Fetch the user instance and assign it to the employee
#             user_id = request.POST.get('user')
#             assigned_user = User.objects.get(id=user_id)
#             instance.user = assigned_user
#
#             # Assign other fields directly from the form data
#             instance.title = request.POST.get('title')
#             instance.image = request.FILES.get('image')
#             instance.firstname = request.POST.get('firstname')
#             instance.lastname = request.POST.get('lastname')
#             instance.othername = request.POST.get('othername')
#             instance.birthday = request.POST.get('birthday')
#
#             # Fetch and assign the role instance
#             role_id = request.POST.get('role')
#             role_instance = Role.objects.get(id=role_id)
#             instance.role = role_instance
#
#             instance.startdate = request.POST.get('startdate')
#             instance.employeetype = request.POST.get('employeetype')
#             instance.employeeid = request.POST.get('employeeid')
#             instance.dateissued = request.POST.get('dateissued')
#
#             # Fetch and assign the department instance
#             department_id = request.POST.get('designation')
#             department_instance = Department.objects.get(id=department_id)
#             instance.designation = department_instance
#
#             instance.save()
#             messages.success(request, 'Employee successfully created ', extra_tags='alert alert-warning alert-dismissible show')
#             return redirect('dashboard:employees')
#         else:
#             messages.error(request, 'Trying to create duplicate employees with a single user account ', extra_tags='alert alert-warning alert-dismissible show')
#             return redirect('dashboard:employeecreate')
#
#     dataset = {'form': EmployeeCreateForm(), 'title': 'register employee'}
#     return render(request, 'dashboard/employee_create.html', dataset)
#
#


def dashboard_employees_create(request):
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
        return redirect('/')

    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.POST.get('user')
            assigned_user = User.objects.get(id=user)

            instance.user = assigned_user

            instance.title = request.POST.get('title')
            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')

            instance.birthday = request.POST.get('birthday')

            role = request.POST.get('role')
            role_instance = Role.objects.get(id=role)
            instance.role = role_instance

            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')
            instance.employeeid = request.POST.get('employeeid')
            instance.dateissued = request.POST.get('dateissued')
            # instance.designation = request.POST.get('designation')

            instance.save()
            messages.success(request, 'Employee successfully created ',
                             extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:employees')
        else:
            messages.error(request, 'Trying to create duplicate employees with a single user account ',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:employeecreate')

    dataset = dict()
    form = EmployeeCreateForm()
    dataset['form'] = form
    dataset['title'] = 'register employee'
    return render(request, 'dashboard/employee_create.html', dataset)


from django.shortcuts import render, redirect
from django.contrib import messages
from employee.forms import FamilyCreateForm
from employee.models import Family
from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required
from employee.models import Employee


@login_required
def dashboard_family_create(request):
    if request.method == 'POST':
        form = FamilyCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user

            # Associate the family record with the selected employee
            employee_id = request.POST.get('employee')
            if employee_id:
                instance.employee_id = employee_id

            instance.save()
            messages.success(request, 'Family information successfully created',
                             extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:family')
        else:
            messages.error(request, 'Invalid input. Please check your information.',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:familycreate')

    form = FamilyCreateForm()
    employees = Employee.objects.all()
    users = User.objects.all()
    dataset = {'form': form, 'title': 'Add Family Information', 'employees': employees, 'users': users}
    return render(request, 'dashboard/family_create.html', dataset)


#
# @login_required
# def dashboard_family_create(request):
#     if request.method == 'POST':
#         form = FamilyCreateForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = request.user
#             instance.save()
#             messages.success(request, 'Family information successfully created',
#                              extra_tags='alert alert-warning alert-dismissible show')
#             return redirect('dashboard:family')
#
#         else:
#             messages.error(request, 'Invalid input. Please check your information.',
#                            extra_tags='alert alert-warning alert-dismissible show')
#             return redirect('dashboard:familycreate')
#
#     form = FamilyCreateForm()
#     employees = Employee.objects.all()  # Fetch all employees from the database
#     family = Family.objects.all()
#     users = User.objects.all()
#     dataset = {'form': form, 'title': 'Add Family Information', 'employees': employees, 'family':family, 'users':users}
#     return render(request, 'dashboard/family_create.html', dataset)

from django.shortcuts import render
from employee.models import Family
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_family(request):
    family_info = Family.objects.filter(user=request.user).first()
    spouse = Family.objects.filter(user=request.user).first()
    status = Family.objects.filter(user=request.user).first()
    occupation = Family.objects.filter(user=request.user).first()
    context = {
        'family': family_info,
        'spouse': spouse,
        'status': status,
        'occupation': occupation,
        # 'error':error
        # tel
        # children
        # nextofkin
        # contact
        # relationship
        # father
        # foccupation
        # mother
        # moccupation

    }
    return render(request, 'dashboard/family.html', context)


def employee_edit_data(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser or request.user.is_staff):
        return redirect('/')
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST or None, request.FILES or None, instance=employee)
        if form.is_valid():
            instance = form.save(commit=False)

            user = request.POST.get('user')
            assigned_user = User.objects.get(id=user)

            instance.user = assigned_user

            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')

            instance.birthday = request.POST.get('birthday')

            religion_id = request.POST.get('religion')
            religion = Religion.objects.get(id=religion_id)
            instance.religion = religion

            nationality_id = request.POST.get('nationality')
            nationality = Nationality.objects.get(id=nationality_id)
            instance.nationality = nationality

            department_id = request.POST.get('department')
            department = Department.objects.get(id=department_id)
            instance.department = department

            instance.hometown = request.POST.get('hometown')
            instance.region = request.POST.get('region')
            instance.residence = request.POST.get('residence')
            instance.address = request.POST.get('address')
            instance.education = request.POST.get('education')
            instance.lastwork = request.POST.get('lastwork')
            instance.position = request.POST.get('position')
            instance.ssnitnumber = request.POST.get('ssnitnumber')
            instance.tinnumber = request.POST.get('tinnumber')

            role = request.POST.get('role')
            role_instance = Role.objects.get(id=role)
            instance.role = role_instance

            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')
            instance.employeeid = request.POST.get('employeeid')
            instance.dateissued = request.POST.get('dateissued')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()
            messages.success(request, 'Account Updated Successfully !!!',
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:employees')

        else:

            messages.error(request, 'Error Updating account', extra_tags='alert alert-warning alert-dismissible show')
            return HttpResponse("Form data not valid")

    dataset = dict()
    form = EmployeeCreateForm(request.POST or None, request.FILES or None, instance=employee)
    dataset['form'] = form
    dataset['title'] = 'edit - {0}'.format(employee.get_full_name)
    return render(request, 'dashboard/employee_create.html', dataset)


from django.shortcuts import render, redirect
from django.contrib import messages
from employee.forms import EmergencyCreateForm
from employee.models import Emergency
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_emergency_create(request):
    if request.method == 'POST':
        form = EmergencyCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user

            # Associate the emergency record with the selected employee
            employee_id = request.POST.get('employee')
            if employee_id:
                instance.employee_id = employee_id
            else:
                messages.error(request, 'Please select an employee.', extra_tags='alert alert-warning alert-dismissible show')
                return redirect('dashboard:emergencycreate')

            instance.save()

            messages.success(request, 'Emergency information successfully created',
                             extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:emergency')

        else:
            messages.error(request, 'Invalid input. Please check your information.',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:emergencycreate')

    form = EmergencyCreateForm()
    employees = Employee.objects.all()  # Fetch all employees from the database
    dataset = {'form': form, 'title': 'Add Emergency Information', 'employees': employees}
    return render(request, 'dashboard/emergency_create.html', dataset)

# @login_required
# def dashboard_emergency_create(request):
#     if request.method == 'POST':
#         form = EmergencyCreateForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = request.user
#
#             # Associate the family record with the selected employee
#             employee_id = request.POST.get('employee')
#             if employee_id:
#                 instance.employee_id = employee_id
#
#             instance.save()
#
#             messages.success(request, 'Emergency information successfully created',
#                              extra_tags='alert alert-warning alert-dismissible show')
#             return redirect('dashboard:emergency')
#
#         else:
#             messages.error(request, 'Invalid input. Please check your information.',
#                            extra_tags='alert alert-warning alert-dismissible show')
#             return redirect('dashboard:emergencycreate')
#
#     form = EmergencyCreateForm()
#     dataset = {'form': form, 'title': 'Add Emergency Information'}
#     return render(request, 'dashboard/emergency_create.html', dataset)
#

@login_required
def dashboard_emergency(request):
    emergency_info = Emergency.objects.filter(user=request.user).first()
    if emergency_info:
        dataset = {'emergency_info': emergency_info, 'title': 'Emergency Information'}
        return render(request, 'dashboard/emergency_detail.html', dataset)
    else:
        messages.error(request, 'Emergency information not found for the current user.',
                       extra_tags='alert alert-warning alert-dismissible show')
        return redirect('dashboard:emergency_create')


from django.shortcuts import get_object_or_404
from employee.models import Employee, Family


from django.core.exceptions import ObjectDoesNotExist

def dashboard_employee_info(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    employee = get_object_or_404(Employee, id=id)

    try:
        family = Family.objects.get(employee=employee)
    except Family.MultipleObjectsReturned:
        family = Family.objects.filter(employee=employee).first()

    try:
        emergency = Emergency.objects.get(employee=employee)
    except Emergency.MultipleObjectsReturned:
        emergency = Emergency.objects.filter(employee=employee).first()

    try:
        bank = Bank.objects.get(employee=employee)
    except Bank.DoesNotExist:
        bank = None
    except Bank.MultipleObjectsReturned:
        bank = Bank.objects.filter(employee=employee).first()

    if hasattr(employee, 'get_full_name') and callable(employee.get_full_name):
        title = 'profile - {}'.format(employee.get_full_name())
    else:
        title = 'profile - Unknown'

    dataset = {
        'employee': employee,
        'family': family,
        'emergency': emergency,
        'title': title,
        'bank': bank
    }
    return render(request, 'dashboard/employee_detail.html', dataset)
# def dashboard_employee_info(request,id):
# 	if not request.user.is_authenticated:
# 		return redirect('/')
#
# 	employee = get_object_or_404(Employee, id = id)
# 	family = get_object_or_404(Family, id = id)
#
#
# 	dataset = dict()
# 	dataset['employee'] = employee
# 	dataset['family'] = family
# 	dataset['title'] = 'profile - {0}'.format(employee.get_full_name)
# 	return render(request,'dashboard/employee_detail.html',dataset)


from django.shortcuts import render, redirect
from django.contrib import messages
from employee.forms import BankCreateForm
from employee.models import Bank
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_bank_create(request):
    if request.method == 'POST':
        form = BankCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user

            # Associate the bank account with the selected employee
            employee_id = request.POST.get('employee')
            if employee_id:
                instance.employee_id = employee_id
            else:
                messages.error(request, 'Please select an employee.', extra_tags='alert alert-warning alert-dismissible show')
                return redirect('dashboard:bankcreate')

            instance.save()

            messages.success(request, 'Bank account information successfully created',
                             extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:bank')

        else:
            messages.error(request, 'Invalid input. Please check your information.',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:bankcreate')

    form = BankCreateForm()
    employees = Employee.objects.all()  # Fetch all employees from the database
    dataset = {'form': form, 'title': 'Add Bank Account Information', 'employees': employees}
    return render(request, 'dashboard/bank_create.html', dataset)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employee.models import Bank

@login_required
def dashboard_bank_detail(request):
    # Retrieve bank account details for the logged-in user
    bank = Bank.objects.filter(user=request.user).first()  # Assuming there's only one bank account per user

    dataset = {'bank': bank}
    return render(request, 'dashboard/bank_detail.html', dataset)
# ---------------------LEAVE--------------------------------------from datetime import date
def get_financial_year_start_end(current_date):
    current_year = current_date.year  # helps me in extracting the correct year from current_date function
    financial_year_start = date(current_year, 7, 1)  #setting the financial year start to july 1st of every year
    if current_date.month < 7:  # If the current month is before July, it belongs to the previous financial year
        print('this belongs to the previous financial year')
        financial_year_start = date(current_year - 1, 7,
                                    1)  #If the current month is before July, the financial_year_start is adjusted to July 1st of the previous year. This ensures that the date belongs to the correct financial year.
    financial_year_end = date(current_year + 1, 6,
                              30)  #Sets the financial_year_end variable to June 30th of the next year. This represents the end of the financial year.
    return financial_year_start, financial_year_end


from datetime import timedelta, date


def get_weekdays(start_date, end_date):
    # Calculate the number of weekdays between two dates
    weekdays = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday to Friday (0 to 4)
            weekdays += 1
        current_date += timedelta(days=1)
    return weekdays


def adjust_weekend(end_date):
    # Adjust the end date to the next working day if it's a weekend
    while end_date.weekday() >= 5:  # Saturday or Sunday
        end_date += timedelta(days=1)
    return end_date


def leave_creation(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user = request.user
    financial_year_start, financial_year_end = get_financial_year_start_end(date.today())
    default_leave_days = 30  # You can adjust this if you have a different default value

    # Get the total leave days taken by the user
    total_days_taken = Leave.get_total_days_taken(user, financial_year_start, financial_year_end)
    days_remaining = default_leave_days - total_days_taken

    # Determine if leave application should be disabled
    apply_leave_disabled = days_remaining <= 0

    if request.method == 'POST':
        form = LeaveCreationForm(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user

            # Calculate the adjusted end date that excludes weekends
            adjusted_end_date = adjust_weekend(instance.enddate)

            # Calculate the number of weekdays between start date and adjusted end date
            weekdays = get_weekdays(instance.startdate, adjusted_end_date)

            # Calculate the number of extra days needed to adjust for weekends
            extra_days = weekdays - (adjusted_end_date - instance.startdate).days

            # Adjust the end date by adding the extra days
            instance.enddate += timedelta(days=extra_days)

            instance.save()

            context = {
                'leave': instance,
                'weekdays': weekdays,
                'adjusted_end_date': instance.enddate,
                'apply_leave_disabled': apply_leave_disabled
            }

            messages.success(request, 'Leave Request Sent, wait for Admins response',
                             extra_tags='alert alert-success alert-dismissible show')
            return render(request, 'dashboard/create_leave.html', context)
        messages.error(request, 'Failed to request a Leave, please check entry dates',
                       extra_tags='alert alert-warning alert-dismissible show')

    form = LeaveCreationForm()
    dataset = {
        'form': form,
        'title': 'Apply for Leave',
        'apply_leave_disabled': apply_leave_disabled
    }
    return render(request, 'dashboard/create_leave.html', dataset)



def leaves_list(request):
    leaves = Leave.objects.all_pending_leaves()
    return render(request, 'dashboard/leaves_recent.html', {'leave_list': leaves, 'title': 'Leaves List - Pending'})


# def pending_recommendation(request):
#     leaves = Leave.objects.all_pending_leaves_to_be_recommended_leaves()
#     return render(request, 'dashboard/recommendation_recent.html', {'leave_list': leaves, 'title': 'Leaves List - Pending Recommendation'})


def Unrecommend_list(request):
    leaves = Leave.objects.all_unrecommended_leaves()
    return render(request, 'dashboard/unrecommended.html',
                  {'leave_list': leaves, 'title': 'Leaves List - Unrecommended'})


def edit_leave(request, id):
    # Retrieve the existing Leave object
    leave = Leave.objects.get(id=id)
    if request.method == 'POST':
        # Handle the form submission or input data for updating leave details
        form = LeaveCreationForm(data=request.POST, instance=leave)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave details updated successfully.')
            return redirect('dashboard:leave_detail', id=id)
        else:
            messages.error(request, 'Failed to update leave details. Please check the form.')

    else:
        # If it's a GET request, populate the form with existing leave data
        form = LeaveCreationForm(instance=leave)

    context = {
        'form': form,
        'title': 'Edit Leave',
    }
    return render(request, 'dashboard/edit_leave.html', context)


from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from leave.models import Leave


def update_leave_end_date(request, id):
    if not request.user.is_authenticated and request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    if not request.user.is_staff:
        return redirect('dashboard:leaves')  # Redirect if not a staff member
    if request.method == 'POST':
        new_end_date = request.POST.get('enddate')
        try:
            # Attempt to update the leave end date
            leave.enddate = new_end_date
            leave.save()
        except ValidationError:
            error_message = "Check your date input well"
            return render(request, 'dashboard/update_leave_end_date.html',
                          {'leave': leave, 'error_message': error_message})

    return render(request, 'dashboard/update_leave_end_date.html', {'leave': leave})

from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from leave.models import Leave, CarriedForward
from employee.models import Employee

def get_financial_year_start_end(current_date):
    financial_year_start = date(current_date.year, 7, 1)
    financial_year_end = date(current_date.year + 1, 6, 30)
    return financial_year_start, financial_year_end

def leaves_view(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    user = request.user
    leave = get_object_or_404(Leave, id=id)
    employee = Employee.objects.filter(user=leave.user).first()

    # Fetch the related Holiday object
    holiday = leave.holiday if hasattr(leave, 'holiday') else None
    holiday_name = holiday.holiday_name if holiday else 'Not yet updated'
    holiday_type = holiday.holiday_type if holiday else 'Not yet updated'
    holiday_date = holiday.holiday_date if holiday else 'Not yet updated'

    # Calculate carried forward days
    try:
        carried_forward = CarriedForward.objects.get(user=leave.user)
        carried_forward_days = carried_forward.leave_days_carried_forward
    except CarriedForward.DoesNotExist:
        carried_forward_days = 0

    # Ensure carried_forward_days does not exceed the maximum limit
    carried_forward_days = min(carried_forward_days, 15)

    # Calculate total leave days available
    total_leave_days_available = 30 + carried_forward_days

    # Calculate leave days applied for the current leave
    leave_days_applied = (leave.enddate - leave.startdate).days

    # Fetch approved leaves within the current financial year
    financial_year_start, financial_year_end = get_financial_year_start_end(date.today())
    total_days_taken = Leave.get_total_days_taken(leave.user, financial_year_start, financial_year_end)

    # Calculate total leave days remaining
    total_leave_days_remaining = total_leave_days_available - total_days_taken

    context = {
        'leave': leave,
        'employee': employee,
        'carried_forward_days': carried_forward_days,
        'total_leave_days_available': total_leave_days_available,
        'leave_days_applied': leave_days_applied,
        'total_days_taken': total_days_taken,
        'total_leave_days_remaining': total_leave_days_remaining,
        'title': '{0}-{1} leave'.format(leave.user.username, leave.status),
        'holiday_name': holiday_name,
        'holiday_type': holiday_type,
        'holiday_date': holiday_date,
    }
    return render(request, 'dashboard/leave_detail_view.html', context)

from datetime import timedelta, date
from django.shortcuts import render, redirect, get_object_or_404
from leave.models import Leave, CarriedForward
from employee.models import Employee
from leave.models import Holiday

from datetime import timedelta

from datetime import date, timedelta

from django.shortcuts import get_object_or_404, render, redirect
from datetime import date, timedelta


# def get_financial_year_start_end(current_date):
#     if current_date.month > 6:  # Assuming financial year starts in July
#         financial_year_start = date(current_date.year, 7, 1)
#         financial_year_end = date(current_date.year + 1, 6, 30)
#     else:
#         financial_year_start = date(current_date.year - 1, 7, 1)
#         financial_year_end = date(current_date.year, 6, 30)
#     return financial_year_start, financial_year_end

# from datetime import date
# from django.shortcuts import render, redirect, get_object_or_404
# from leave.models import Leave, CarriedForward
# from employee.models import Employee
# def get_financial_year_start_end(current_date):
#     financial_year_start = date(current_date.year, 7, 1)
#     financial_year_end = date(current_date.year + 1, 6, 30)
#     return financial_year_start, financial_year_end
#
# def leaves_view(request, id):
#     if not request.user.is_authenticated:
#         return redirect('/')
#
#     user = request.user
#     leave = get_object_or_404(Leave, id=id)
#     employee = Employee.objects.filter(user=leave.user).first()
#
#     # Fetch the related Holiday object
#     holiday = leave.holiday if hasattr(leave, 'holiday') else None
#     holiday_name = holiday.holiday_name if holiday else 'Not yet updated'
#     holiday_type = holiday.holiday_type if holiday else 'Not yet updated'
#     holiday_date = holiday.holiday_date if holiday else 'Not yet updated'
#
#     # Calculate carried forward days
#     try:
#         carried_forward = CarriedForward.objects.get(user=leave.user)
#         carried_forward_days = carried_forward.leave_days_carried_forward
#     except CarriedForward.DoesNotExist:
#         carried_forward_days = 0
#
#     # Ensure carried_forward_days does not exceed the maximum limit
#     carried_forward_days = min(carried_forward_days, 15)
#
#     # Calculate total leave days available
#     total_leave_days_available = 30 + carried_forward_days
#
#     # Calculate total leave days taken for the current leave object
#     total_leave_days_taken = (leave.enddate - leave.startdate).days
#
#     # Fetch approved leaves within the current financial year
#     financial_year_start, financial_year_end = get_financial_year_start_end(date.today())
#     total_days_taken = Leave.get_total_days_taken(user, financial_year_start, financial_year_end)
#
#     # Calculate total leave days remaining
#     total_leave_days_remaining = total_leave_days_available - total_days_taken - total_leave_days_taken
#
#     context = {
#         'leave': leave,
#         'employee': employee,
#         'carried_forward_days': carried_forward_days,
#         'total_leave_days_available': total_leave_days_available,
#         'total_leave_days_taken': total_leave_days_taken,
#         'total_days_taken': total_days_taken,
#         'total_leave_days_remaining': total_leave_days_remaining,
#         'title': '{0}-{1} leave'.format(leave.user.username, leave.status),
#         'holiday_name': holiday_name,
#         'holiday_type': holiday_type,
#         'holiday_date': holiday_date,
#     }
#     return render(request, 'dashboard/leave_detail_view.html', context)

# def leaves_view(request, id):
#     if not request.user.is_authenticated:
#         return redirect('/')
#
#     user = request.user
#     leave = get_object_or_404(Leave, id=id)
#     employee = Employee.objects.filter(user=leave.user).first()
#
#     # Fetch the related Holiday object
#     holiday = leave.holiday if hasattr(leave, 'holiday') else None
#     holiday_name = holiday.holiday_name if holiday else 'Not yet updated'
#     holiday_type = holiday.holiday_type if holiday else 'Not yet updated'
#     holiday_date = holiday.holiday_date if holiday else 'Not yet updated'
#
#     try:
#         carried_forward = CarriedForward.objects.get(user=leave.user)
#         carried_forward_days = carried_forward.leave_days_carried_forward
#     except CarriedForward.DoesNotExist:
#         carried_forward_days = 0
#
#     # Calculate total leave days available
#     total_leave_days_available = 30 + carried_forward_days
#
#     # Calculate total leave days taken for the current leave object
#     total_leave_days_taken = (leave.enddate - leave.startdate).days
#
#     # Fetch approved leaves within the current financial year
#     financial_year_start, financial_year_end = get_financial_year_start_end(date.today())
#     total_days_taken = Leave.get_total_days_taken(user, financial_year_start, financial_year_end)
#
#     # Calculate total leave days remaining
#     total_leave_days_remaining = total_leave_days_available - total_days_taken - total_leave_days_taken
#
#     # Ensure carried_forward_days does not exceed the maximum limit
#     carried_forward_days = min(carried_forward_days, 15)
#
#     context = {
#         'leave': leave,
#         'employee': employee,
#         'carried_forward_days': carried_forward_days,
#         'total_leave_days_available': total_leave_days_available,
#         'total_leave_days_taken': total_leave_days_taken,
#         'total_days_taken': total_days_taken,
#         'total_leave_days_remaining': total_leave_days_remaining,
#         'title': '{0}-{1} leave'.format(leave.user.username, leave.status),
#         'holiday_name': holiday_name,
#         'holiday_type': holiday_type,
#         'holiday_date': holiday_date,
#     }
#     return render(request, 'dashboard/leave_detail_view.html', context)


# def leaves_view(request, id):
#     if not request.user.is_authenticated:
#         return redirect('/')
#
#     user = request.user
#     leave = get_object_or_404(Leave, id=id)
#     employee = Employee.objects.filter(user=leave.user).first()
#
#     # Fetch the related Holiday object
#     holiday = leave.holiday if hasattr(leave, 'holiday') else None
#     holiday_name = holiday.holiday_name if holiday else 'Not yet updated'
#     holiday_type = holiday.holiday_type if holiday else 'Not yet updated'
#     holiday_date = holiday.holiday_date if holiday else 'Not yet updated'
#
#     try:
#         carried_forward = CarriedForward.objects.get(user=leave.user)
#         carried_forward_days = carried_forward.leave_days_carried_forward
#     except CarriedForward.DoesNotExist:
#         carried_forward_days = 0
#
#     # Calculate total leave days available
#     total_leave_days_available = 30 + carried_forward_days
#
#     # Calculate total leave days taken for the current leave object
#     total_leave_days_taken = (leave.enddate - leave.startdate).days
#
#     # Calculate total leave days remaining
#     total_leave_days_remaining = total_leave_days_available - total_leave_days_taken
#     carried_forward_days = min(carried_forward_days, 15)
#
#     # Check if the user is a staff member
#     is_staff = request.user.is_staff
#
#     # Store the original end date
#     original_end_date = leave.enddate
#
#     # Initialize adjusted_end_date with the original end date
#     adjusted_end_date = original_end_date
#
#     if adjusted_end_date is not None:
#         current_date = leave.startdate
#         business_days_to_add = 0  # Count of business days (weekdays) to add
#
#         while business_days_to_add < total_leave_days_taken:
#             # Check if the current_date is a weekday (Monday to Friday)
#             if current_date.weekday() < 5:
#                 business_days_to_add += 1
#
#             # Move to the next day
#             current_date += timedelta(days=1)
#
#             # Check if the adjusted_end_date is a weekend (Saturday or Sunday)
#             if adjusted_end_date.weekday() >= 5:
#                 # Move the adjusted_end_date to the next Monday (weekday)
#                 adjusted_end_date += timedelta(days=(7 - adjusted_end_date.weekday()))
#
#     # Fetch approved leaves within the current financial year
#     approved_leaves = Leave.objects.filter(user=user, is_approved=True)
#     financial_year_start, financial_year_end = get_financial_year_start_end(date.today())
#
#     # Calculate total leave days taken within the current financial year
#     total_days_taken = sum(
#         (leave.enddate - leave.startdate).days for leave in approved_leaves
#         if financial_year_start <= leave.startdate <= financial_year_end
#     )
#
#     context = {
#         'leave': leave,
#         'employee': employee,
#         'carried_forward_days': carried_forward_days,
#         'total_leave_days_available': total_leave_days_available,
#         'total_leave_days_taken': total_leave_days_taken,
#         'total_days_taken': total_days_taken,
#         'total_leave_days_remaining': total_leave_days_remaining,
#         'is_staff': is_staff,
#         'adjusted_end_date': adjusted_end_date,
#         'title': '{0}-{1} leave'.format(leave.user.username, leave.status),
#         'holiday_name': holiday_name,
#         'holiday_type': holiday_type,
#         'holiday_date': holiday_date,
#     }
#     return render(request, 'dashboard/leave_detail_view.html', context)
#

# def leaves_view(request, id):
#     if not request.user.is_authenticated:
#         return redirect('/')
#     user = request.user
#
#     leave = get_object_or_404(Leave, id=id)
#     employee = Employee.objects.filter(user=leave.user).first()
#
#     # Fetch the related Holiday object
#     holiday = leave.holiday if hasattr(leave, 'holiday') else None
#     holiday_name = holiday.holiday_name if holiday else 'Not yet updated'
#     holiday_type = holiday.holiday_type if holiday else 'Not yet updated'
#     holiday_date = holiday.holiday_date if holiday else 'Not yet updated'
#
#     try:
#         carried_forward = CarriedForward.objects.get(user=leave.user)
#         carried_forward_days = carried_forward.leave_days_carried_forward
#     except CarriedForward.DoesNotExist:
#         carried_forward_days = 0
#
#     # Calculate total leave days available
#     total_leave_days_available = 30 + carried_forward_days
#
#     # Calculate total leave days taken
#     total_leave_days_taken = leave.total_leave_days_taken
#
#     # Calculate total leave days remaining
#     total_leave_days_remaining = total_leave_days_available - total_leave_days_taken
#     carried_forward_days = min(carried_forward_days, 15)
#
#     # Check if the user is a staff member
#     is_staff = request.user.is_staff
#
#     # Store the original end date
#     original_end_date = leave.enddate
#
#     # Initialize adjusted_end_date with the original end date
#     adjusted_end_date = original_end_date
#
#     if adjusted_end_date is not None:
#         current_date = leave.startdate
#         business_days_to_add = 0  # Count of business days (weekdays) to add
#
#         while business_days_to_add < total_leave_days_taken:
#             # Check if the current_date is a weekday (Monday to Friday)
#             if current_date.weekday() < 5:
#                 business_days_to_add += 1
#
#             # Move to the next day
#             current_date += timedelta(days=1)
#
#             # Check if the adjusted_end_date is a weekend (Saturday or Sunday)
#             if adjusted_end_date.weekday() >= 5:
#                 # Move the adjusted_end_date to the next Monday (weekday)
#                 adjusted_end_date += timedelta(days=(7 - adjusted_end_date.weekday()))
#     approved_leaves = Leave.objects.filter(user=user, is_approved=True)
#
#     financial_year_start, financial_year_end = get_financial_year_start_end(date.today())
#
#     # Ensure adjusted_end_date is on or after the original end date
#     # adjusted_end_date = max(original_end_date, adjusted_end_date)
#     total_days_taken = sum((leave.enddate - leave.startdate).days for leave in approved_leaves
#                            if financial_year_start <= leave.startdate <= financial_year_end)
#     print("Total days taken within the current financial year:", total_days_taken)
#     context = {
#         'leave': leave,
#         'employee': employee,
#         'carried_forward_days': carried_forward_days,
#         'total_leave_days_available': total_leave_days_available,
#         'total_leave_days_taken': total_leave_days_taken,
#         'total_days_taken': total_days_taken,
#         'total_leave_days_remaining': total_leave_days_remaining,
#         'is_staff': is_staff,
#         'adjusted_end_date': adjusted_end_date,
#         'title': '{0}-{1} leave'.format(leave.user.username, leave.status),
#         'holiday_name': holiday_name,
#         'holiday_type': holiday_type,
#         'holiday_date': holiday_date,
#     }
#     return render(request, 'dashboard/leave_detail_view.html', context)


from django.http import HttpResponseRedirect
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from leave.models import Leave
from leave.models import Holiday
from accounts.forms import HolidayForm

from django.http import HttpResponseRedirect


def add_holiday_view(request, id):
    if not request.user.is_authenticated or (not request.user.is_staff and not request.user.is_superuser):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    holiday_name = 'Not yet updated'
    holiday_type = 'Not yet updated'
    holiday_date = 'Not yet updated'

    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            holiday = form.save(commit=False)
            holiday_name = holiday.holiday_name
            holiday_type = holiday.holiday_type
            holiday_date = holiday.holiday_date
            holiday.save()

            # Update adjusted_end_date based on the new holiday
            adjusted_end_date = leave.enddate
            days_to_add = 0
            current_date = leave.startdate
            while current_date <= adjusted_end_date:
                if current_date.weekday() >= 5:  # Saturday (5) or Sunday (6)
                    days_to_add += 2
                if current_date == holiday_date:
                    days_to_add += 1
                current_date += timedelta(days=1)
            adjusted_end_date += timedelta(days=days_to_add)

            leave.enddate = adjusted_end_date
            leave.save()
            return redirect('dashboard:userleaveview', id=id)
        else:
            print('Form is Not Valid', form.errors)

    form = HolidayForm()
    context = {
        'leave': leave,
        'form': form,
        'title': 'Add Holiday for Leave Adjustment',
        'holiday_date': holiday_date,
        'holiday_name': holiday_name,
        'holiday_type': holiday_type,
    }
    print(Holiday.holiday_name)
    print(Holiday.holiday_date)
    print(holiday_type)
    return render(request, 'dashboard/add_holiday.html', context)


def recommend_view(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    print(leave.user)

    # Check if there are any results in the queryset
    employees = Employee.objects.filter(user=leave.user)
    if employees.exists():
        employee = employees[0]  # Access the first element if it exists
        print(employee)
    else:
        # Handle the case where no employees are found for the given user
        # You can return an error message or handle it as appropriate for your application
        print("No employee found for user:", leave.user)

    return render(request, 'dashboard/leave_recommended_view.html', {
        'leave': leave,
        'employee': employee if employees.exists() else None,  # Pass None if no employees are found
        'title': '{0}-{1} leave'.format(leave.user.username, leave.status)
    })


from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


def approve_leave(request, id):
    if not (request.user.is_superuser or (request.user.is_staff and request.user.is_authenticated)):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    user = leave.user

    try:
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        # Handle the case where the Employee does not exist
        error_message = "We couldn't find the employee associated with this leave request. Please contact your administrator for assistance."
        return HttpResponse(error_message)

    leave.approve_leave()
    print('i have been approved')

    messages.success(request, 'Leave successfully approved for {0}'.format(employee.get_full_name),
                     extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:userleaveview', id=id)


def recommend_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_staff and not request.user.is_superuser):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)

    if leave.status == 'pending':
        # Update status to 'recommended'
        leave.status = 'recommended'
        leave.save()

        # Get user and employee information
        user = leave.user
        employee = Employee.objects.filter(user=user).first()

        # Print a message
        print('Leave request has been recommended')

        # Add a success message
        messages.success(request, 'Leave successfully recommended for {0}'.format(employee.get_full_name),
                         extra_tags='alert alert-success alert-dismissible show')

        # Redirect to the recommended view
        return redirect('dashboard:userrecommendview', id=id)
    else:
        # Handle cases where leave is not pending (optional)
        messages.warning(request, 'Leave request cannot be recommended as it is not in pending status',
                         extra_tags='alert alert-warning alert-dismissible show')
        return redirect('dashboard:userrecommendview', id=id)


#supervisor who is staff should see this
def cancel_leaves_list(request):
    if not (request.user.is_superuser or request.user.is_staff and request.user.is_authenticated):
        return redirect('/')
    leaves = Leave.objects.all_cancel_leaves()
    return render(request, 'dashboard/leaves_cancel.html', {'leave_list_cancel': leaves, 'title': 'Cancel leave list'})


#supervisor who is staff should see this
def unapprove_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser or request.user.is_staff):
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    leave.unapprove_leave
    return redirect('dashboard:leaveslist')  #redirect to unapproved list


def leaves_approved_list(request):
    if request.user.is_authenticated:
        leaves = Leave.objects.all_approved_leaves()
        return render(request, 'dashboard/leaves_approved.html', {'leave_list': leaves, 'title': 'Approved Leave List'})
    else:
        return HttpResponse("You need to log in to access this page.")


def recommended_leave_list(request):
    if request.user.is_authenticated:
        leaves = Leave.objects.all_recommended_leaves()
        return render(request, 'dashboard/leaves_recommended.html',
                      {'leave_list': leaves, 'title': 'Recommended Leave List'})
    else:
        return HttpResponse("You need to log in to access this page.")


#supervisor who is staff should see this
def cancel_leave(request, id):
    if not (request.user.is_superuser or request.user.is_staff and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    leave.leaves_cancel

    messages.success(request, 'Leave is canceled', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')  #work on redirecting to instance leave - detail view


# Current section -> here
def uncancel_leave(request, id):
    if not (request.user.is_superuser or request.user.is_staff and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request, 'Leave is uncanceled,now in pending list',
                     extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')  #work on redirecting to instance leave - detail view


#supervisor who is staff should see this
def leave_rejected_list(request):
    dataset = dict()
    leave = Leave.objects.all_rejected_leaves()

    dataset['leave_list_rejected'] = leave
    return render(request, 'dashboard/rejected_leaves_list.html', dataset)


#supervisor who is staff should see this but can be overridden by admin
def reject_leave(request, id):
    dataset = dict()
    leave = get_object_or_404(Leave, id=id)
    leave.reject_leave
    messages.success(request, 'Leave is rejected', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:leavesrejected')


# return HttpResponse(id)


def unreject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request, 'Leave is now in pending list ', extra_tags='alert alert-success alert-dismissible show')

    return redirect('dashboard:leavesrejected')


#  staffs leaves table user only

from django.contrib import messages


# from django.contrib import messages
# from datetime import date
# from .models import Leave, Employee
# from .utils import get_financial_year_start_end  # Import your utility function



from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date, timedelta

def get_financial_year_start_end(current_date):
    if current_date.month > 6:  # Assuming financial year starts in July
        financial_year_start = date(current_date.year, 7, 1)
        financial_year_end = date(current_date.year + 1, 6, 30)
    else:
        financial_year_start = date(current_date.year - 1, 7, 1)
        financial_year_end = date(current_date.year, 6, 30)
    return financial_year_start, financial_year_end


from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date, timedelta


def get_financial_year_start_end(current_date):
    if current_date.month > 6:  # Assuming financial year starts in July
        financial_year_start = date(current_date.year, 7, 1)
        financial_year_end = date(current_date.year + 1, 6, 30)
    else:
        financial_year_start = date(current_date.year - 1, 7, 1)
        financial_year_end = date(current_date.year, 6, 30)
    return financial_year_start, financial_year_end


def view_my_leave_table(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user = request.user
    financial_year_start, financial_year_end = get_financial_year_start_end(date.today())
    default_leave_days = 30

    if user.is_staff:
        leaves = Leave.objects.all()
        users = Employee.objects.all()  # Fetch all employees
    else:
        leaves = Leave.objects.filter(user=user)
        users = [Employee.objects.filter(user=user).first()]

    employee = Employee.objects.filter(user=user).first()

    # Prepare the dataset for each user
    user_leave_data = []
    for emp in users:
        total_days_taken = Leave.get_total_days_taken(emp.user, financial_year_start, financial_year_end)
        days_remaining = default_leave_days - total_days_taken
        leave_details = [{
            'leavetype': leave.leavetype,
            'days_taken': (leave.enddate - leave.startdate).days if leave.is_approved else 0,
            'status': leave.status,
            'id': leave.id
        } for leave in leaves if leave.user == emp.user]

        user_leave_data.append({
            'employee': emp,
            'total_days_taken': total_days_taken,
            'days_remaining': days_remaining,
            'apply_leave_disabled': days_remaining <= 0,
            'leave_details': leave_details
        })

    dataset = {
        'leave_list': leaves,
        'employee': employee,
        'title': 'Leaves List',
        'user_leave_data': user_leave_data,
    }

    if user.is_staff:
        for data in user_leave_data:
            if data['days_remaining'] <= 7:
                messages.warning(request,
                                 f'{data["employee"].get_full_name}: Leave days are running low. Only {data["days_remaining"]} days remaining.',
                                 extra_tags='alert alert-warning alert-dismissible show')
    else:
        if user_leave_data[0]['days_remaining'] <= 7:
            messages.warning(request,
                             f'Your leave days are running low. Only {user_leave_data[0]["days_remaining"]} days remaining.',
                             extra_tags='alert alert-warning alert-dismissible show')

    return render(request, 'dashboard/staff_leaves_table.html', dataset)


# def view_my_leave_table(request):
#     if not request.user.is_authenticated:
#         return redirect('accounts:login')
#
#     user = request.user
#
#     if user.is_staff:
#         leaves = Leave.objects.all()
#     else:
#         leaves = Leave.objects.filter(user=user)
#
#     employee = Employee.objects.filter(user=user).first()
#
#     financial_year_start, financial_year_end = get_financial_year_start_end(date.today())
#     total_days_taken = Leave.get_total_days_taken(user, financial_year_start, financial_year_end)
#
#     default_leave_days = 30
#     days_remaining = default_leave_days - total_days_taken
#
#     dataset = {
#         'leave_list': leaves,
#         'employee': employee,
#         'title': 'Leaves List',
#         'total_days_taken': total_days_taken,
#         'days_remaining': days_remaining,
#         'apply_leave_disabled': days_remaining <= 0,
#     }
#
#     if days_remaining <= 7:
#         messages.warning(request, f'Your leave days are running low. Only {days_remaining} days remaining.',
#                          extra_tags='alert alert-warning alert-dismissible show')
#
#     return render(request, 'dashboard/staff_leaves_table.html', dataset)

# def view_my_leave_table(request):
#     if not request.user.is_authenticated:
#         return redirect('accounts:login')
#
#     user = request.user
#
#     if user.is_staff:
#         leaves = Leave.objects.all()
#     else:
#         leaves = Leave.objects.filter(user=user)
#
#     employee = Employee.objects.filter(user=user).first()
#     approved_leaves = Leave.objects.filter(user=user, is_approved=True)
#
#     financial_year_start, financial_year_end = get_financial_year_start_end(date.today())
#
#     # Calculate total days taken from approved leaves within the current financial year
#     total_days_taken = Leave.get_total_days_taken(user, financial_year_start, financial_year_end)
#
#     default_leave_days = 30  # Replace with the appropriate value for your application
#     days_remaining = default_leave_days - total_days_taken
#
#     # Add a variable to the dataset to indicate whether the "Apply Leave" button should be disabled
#     dataset = {
#         'leave_list': leaves,
#         'employee': employee,
#         'title': 'Leaves List',
#         'total_days_taken': total_days_taken,  # Adding total_days_taken to the context
#         'days_remaining': days_remaining,  # Adding days_remaining to the context
#         'apply_leave_disabled': days_remaining <= 0,  # True if no leave days remaining, else False
#     }
#
#     # Check if days_remaining is less than or equal to 7 and raise an alert
#     if days_remaining <= 7:
#         messages.warning(request, f'Your leave days are running low. Only {days_remaining} days remaining.',
#                          extra_tags='alert alert-warning alert-dismissible show')
#
#     return render(request, 'dashboard/staff_leaves_table.html', dataset)

# def view_my_leave_table(request):
#     if request.user.is_authenticated:
#         user = request.user
#
#         if user.is_staff:
#             leaves = Leave.objects.all()
#         else:
#             leaves = Leave.objects.filter(user=user)
#
#         employee = Employee.objects.filter(user=user).first()
#         approved_leaves = Leave.objects.filter(user=user, is_approved=True)
#
#         financial_year_start, financial_year_end = get_financial_year_start_end(date.today())
#
#         # Calculate total days taken from approved leaves within the current financial year
#         financial_year_start, financial_year_end = get_financial_year_start_end(date.today())
#         total_days_taken = Leave.get_total_days_taken(user, financial_year_start, financial_year_end)
#
#         default_leave_days = 30  # Replace with the appropriate value for your application
#         days_remaining = default_leave_days - total_days_taken
#
#         # Add a variable to the dataset to indicate whether the "Apply Leave" button should be disabled
#         dataset = {
#             'leave_list': leaves,
#             'employee': employee,
#             'title': 'Leaves List',
#             'total_days_taken': total_days_taken,  # Adding total_days_taken to the context
#             'days_remaining': days_remaining,  # Adding days_remaining to the context
#             'apply_leave_disabled': days_remaining <= 0,  # True if no leave days remaining, else False
#         }
#
#         # Check if days_remaining is less than or equal to 7 and raise an alert
#         if days_remaining <= 7:
#             messages.warning(request, f'Your leave days are running low. Only {days_remaining} days remaining.',
#                              extra_tags='alert alert-warning alert-dismissible show')
#
#         # Calculate total days taken from all approved leaves within the current financial year
#         total_days_taken_all = sum((leave.enddate - leave.startdate).days for leave in approved_leaves
#                                    if financial_year_start <= leave.startdate <= financial_year_end)
#         print("Total days taken from all leaves within the current financial year:", total_days_taken_all)
#
#         dataset['total_days_taken_all'] = total_days_taken_all  # Add total_days_taken_all to the dataset
#
#     else:
#         return redirect('accounts:login')
#
#     return render(request, 'dashboard/staff_leaves_table.html', dataset)
