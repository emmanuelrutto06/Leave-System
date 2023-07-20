from django.urls import path
from .import views


app_name = 'dashboard'

urlpatterns = [
    path('welcome/',views.dashboard,name='dashboard'),

    # Employee
    path('employees/all/',views.dashboard_employees, name='employees'),
    path('employee/create/',views.dashboard_employees_create, name='employeecreate'),
    path('employee/profile/<int:id>/',views.dashboard_employee_info, name='employeeinfo'),
    path('employee/profile/edit/<int:id>/',views.employee_edit_data, name='edit'),

    # # Emergency
    # path('emergency/create/',views.dashboard_emergency_create,name='emergencycreate'),
    # path('emergency/update/<int:id>',views.dashboard_emergency_update,name='emergencyupdate'),

    # # Family
    # path('family/create/',views.dashboard_family_create,name='familycreate'),
    # path('family/edit/<int:id>',views.dashboard_family_edit,name='familyedit'),
    
    # #Bank
    # path('bank/create/',views.dashboard_bank_create,name='bankaccountcreate'),

    #---work-on-edit-view------#
    # path('bank/edit/<int:id>/',views.employee_bank_account_update,name='accountedit'),
    path('leave/apply/',views.leave_creation,name='createleave'),
    path('leaves/pending/all/',views.leaves_list,name='leaveslist'),
    path('leaves/approved/all/',views.leaves_approved_list,name='approvedleaveslist'),
    path('leave/unrecommended/all',views.Unrecommend_list,name='unrecommendedleavelist'),
    path('leaves/all/view/<int:id>/',views.unrecommend_view,name='unrecommendview'),

    path('leaves/cancel/all/',views.cancel_leaves_list,name='canceleaveslist'),
    
    path('leaves/all/view/<int:id>/',views.leaves_view,name='userleaveview'),
    
    path('leaves/recommended/all/',views.recommend_leave_list,name='recommendedleavelist'),
    path('leaves/recommend/view/<int:id>/',views.recommend_view,name='recommendview'),
    path('leave/recommend/<int:id>/',views.recommend_leave,name='userrecommend'),

    path('leaves/view/table/',views.view_my_leave_table,name='staffleavetable'),
    
    path('leave/approve/<int:id>/',views.approve_leave,name='userleaveapprove'),

    
    path('leave/unapprove/<int:id>/',views.unapprove_leave,name='userleaveunapprove'),
    
    path('leave/unrecommendleave/<int:id>/',views.unrecommend_leave,name='unrecommendleave'),

    path('leave/cancel/<int:id>/',views.cancel_leave,name='userleavecancel'),
    path('leave/uncancel/<int:id>/',views.uncancel_leave,name='userleaveuncancel'),
    path('leaves/rejected/all/',views.leave_rejected_list,name='leavesrejected'),
    path('leave/reject/<int:id>/',views.reject_leave,name='reject'),
    path('leave/unreject/<int:id>/',views.unreject_leave,name='unreject'),
    path('leave/edit/<int:id>/', views.edit_leave, name='edit_leave'),


    # BIRTHDAY ROUTE
    # path('birthdays/all/',views.birthday_this_month,name='birthdays'),



]
