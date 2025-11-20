from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from employee.models import Employee
from leave.models import Leave
import datetime


def index_view(request):
	# Get real statistics data
	employees = Employee.objects.all()
	leaves = Leave.objects.all()
	pending_leaves = Leave.objects.filter(status='pending')
	approved_today = Leave.objects.filter(
		status='approved',
		updated__date__gte=datetime.date.today()
	).count()

	context = {
		'employees': employees,
		'leaves': leaves,
		'pending_leaves': pending_leaves,
		'approved_today': approved_today,
	}

	return render(request,'index.html', context)