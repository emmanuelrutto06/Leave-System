from django.db import models
from .manager import LeaveManager
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from datetime import date
from django.conf import settings
from django.core.validators import MaxValueValidator
from accounts.models import FinancialYear


class Holiday(models.Model):
    HOLIDAY_TYPES = [
        ('public', 'Public Holiday'),
        ('company', 'Company Holiday'),
    ]
    holiday_date = models.DateField(default="YYYY-MM-DD")
    holiday_type = models.CharField(max_length=10, choices=HOLIDAY_TYPES)
    holiday_name = models.CharField(max_length=100, default="To be Updated")  # Add default value

    def __str__(self):
        return f"{self.holiday_type} - {self.holiday_date}"


from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from datetime import date, timedelta

ANNUAL = 'annual'
SICK = 'sick'
CASUAL = 'casual'
EMERGENCY = 'emergency'
STUDY = 'study'
MATERNITY = 'maternity'
BEREAVEMENT = 'bereavement'
QUARANTINE = 'quarantine'
COMPENSATORY = 'compensatory'
SABBATICAL = 'sabbatical'

LEAVE_TYPE = (
    (ANNUAL, 'annual'),
    (SICK, 'Sick Leave'),
    (CASUAL, 'Casual Leave'),
    (EMERGENCY, 'Emergency Leave'),
    (STUDY, 'Study Leave'),
    (MATERNITY, 'Maternity Leave'),
    (BEREAVEMENT, 'Bereavement Leave'),
    (QUARANTINE, 'Self Quarantine'),
    (COMPENSATORY, 'Compensatory Leave'),
    (SABBATICAL, 'Sabbatical Leave')
)

class Leave(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    startdate = models.DateField(verbose_name=_('Start Date'), help_text='leave start date is on ..', null=True, blank=False)
    enddate = models.DateField(verbose_name=_('End Date'), help_text='coming back on ...', null=True, blank=False)
    leavetype = models.CharField(choices=LEAVE_TYPE, max_length=25, default='SICK', null=True, blank=False)
    reason = models.CharField(verbose_name=_('Reason for Leave'), max_length=255, help_text='add additional information for leave', null=True, blank=True)
    default_annual_leave_days = models.PositiveIntegerField(default=30)
    leave_days_taken = models.PositiveIntegerField(default=0)
    leave_days_remaining = models.PositiveIntegerField(default=0)
    total_leave_days_available = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default='pending')
    is_approved = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    holiday = models.ForeignKey('Holiday', on_delete=models.SET_NULL, null=True, blank=True)
    is_recommended = models.BooleanField(default=False)

    objects = LeaveManager()

    class Meta:
        verbose_name = _('Leave')
        verbose_name_plural = _('Leaves')
        ordering = ['-created']

    def __str__(self):
        return '{0} - {1}'.format(self.leavetype, self.user.get_full_name())

    @property
    def total_days(self):
        return (self.enddate - self.startdate).days

    @staticmethod
    def get_total_days_taken(user, start_date, end_date):
        approved_leaves = Leave.objects.filter(user=user, is_approved=True, startdate__gte=start_date, enddate__lte=end_date)
        return sum((leave.enddate - leave.startdate).days for leave in approved_leaves)

    @property
    def pretty_leave(self):
        leave = self.leavetype
        user = self.user
        employee = user.employee_set.first().get_full_name
        return '{0} - {1}'.format(employee, leave)

    @property
    def leave_approved(self):
        return self.is_approved == True

    @property
    def leave_recommended(self):
        return self.status == 'recommended'

    @property
    def leave_pending(self):
        return self.is_approved == True

    def approve_leave(self):
        if not self.is_approved:
            self.is_approved = True
            self.status = 'approved'
            self.save()

    def recommend_leave(self):
        if not self.is_recommended:
            self.is_recommended = True
            self.status = 'recommended'
            self.save()

    def unapprove_leave(self):
        if self.is_approved:
            self.is_approved = False
            self.status = 'pending'
            self.save()

    def unrecommend_leave(self):
        if self.is_recommended:
            self.is_recommended = False
            self.status = 'pending'
            self.save()

    def approve_recommended_leave(self):
        if self.status == 'recommended':
            self.is_approved = True
            self.status = 'recommended'
            self.save()

    def leaves_cancel(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'cancelled'
            self.save()

    def reject_leave(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'rejected'
            self.save()

    @property
    def is_rejected(self):
        return self.status == 'rejected'

    @property
    def total_leave_days_taken(self):
        if self.startdate and self.enddate:
            return (self.enddate - self.startdate).days
        return 0

    # @property
    # def total_leave_days_remaining(self):
    #      total_leave_days_remaining = total_leave_days_available - total_days_taken
    #
    #     # return self.total_leave_days_available - self.total_leave_days_taken

# class Leave(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
#     startdate = models.DateField(verbose_name=_('Start Date'), help_text='leave start date is on ..', null=True,
#                                  blank=False)
#     enddate = models.DateField(verbose_name=_('End Date'), help_text='coming back on ...', null=True, blank=False)
#     leavetype = models.CharField(choices=LEAVE_TYPE, max_length=25, default='SICK', null=True, blank=False)
#     reason = models.CharField(verbose_name=_('Reason for Leave'), max_length=255,
#                               help_text='add additional information for leave', null=True, blank=True)
#     default_annual_leave_days = models.PositiveIntegerField(default=30)
#     leave_days_taken = models.PositiveIntegerField(default=0)
#     leave_days_remaining = models.PositiveIntegerField(default=0)
#     total_leave_days_available = models.PositiveIntegerField(default=0)
#     status = models.CharField(max_length=20, default='pending')
#     is_approved = models.BooleanField(default=False)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
#     holiday = models.ForeignKey('Holiday', on_delete=models.SET_NULL, null=True, blank=True)
#     is_recommended = models.BooleanField(default=False)
#
#     objects = LeaveManager()
#
#     class Meta:
#         verbose_name = _('Leave')
#         verbose_name_plural = _('Leaves')
#         ordering = ['-created']
#
#     def __str__(self):
#         return '{0} - {1}'.format(self.leavetype, self.user.get_full_name())
#
#     @property
#     def total_days(self):
#         return (self.enddate - self.startdate).days
#
#     @staticmethod
#     def get_total_days_taken(user, start_date, end_date):
#         approved_leaves = Leave.objects.filter(user=user, is_approved=True, startdate__gte=start_date,
#                                                enddate__lte=end_date)
#         return sum((leave.enddate - leave.startdate).days for leave in approved_leaves)
#
#     # def __str__(self):
#     #     return '{0} - {1}'.format(self.leavetype, self.user)
#
#     @property
#     def pretty_leave(self):
#         '''
#         i don't like the __str__ of leave object - this is a pretty one :-)
#         '''
#         leave = self.leavetype
#         user = self.user
#         employee = user.employee_set.first().get_full_name
#         return '{0} - {1}'.format(employee, leave)
#
#     @property
#     def leave_approved(self):
#         return self.is_approved == True
#
#     @property
#     def leave_recommended(self):
#         return self.is_recommended == True
#
#     @property
#     def leave_recommended(self):
#         return self.status == 'recommended'
#
#     @property
#     def leave_pending(self):
#         return self.is_approved == True
#
#     # @property
#     def approve_leave(self):
#         if not self.is_approved:
#             self.is_approved = True
#             self.status = 'approved'
#             self.save()
#
#     # if self.status == 'pending':
#     def recommend_leave(self):
#         if not self.is_recommended:
#             self.is_recommended = True  # Marking it as recommended
#             self.status = 'recommended'  # Updating the status to 'recommended'
#             self.save()  # Saving the changes
#
#     @property
#     def unapprove_leave(self):
#         if self.is_approved:
#             self.is_approved = False
#             self.status = 'pending'
#             self.save()
#
#     # @property
#     def unrecommend_leave(self):
#         if self.is_recommended:
#             self.is_recommended = False
#             self.status = 'pending'
#             self.save()
#
#     # @property
#     # def unrecommend_leave(self):
#     #     if self.is_approved:
#     #         self.is_approved = False
#     #         self.status = 'pending'
#     #         self.save()
#
#     def approve_recommended_leave(self):
#         if self.status == 'recommended':
#             self.is_approved = True
#             self.status = 'recommended'
#             self.save()
#
#     @property
#     def leaves_cancel(self):
#         if self.is_approved or not self.is_approved:
#             self.is_approved = False
#             self.status = 'cancelled'
#             self.save()
#
#     @property
#     def reject_leave(self):
#         if self.is_approved or not self.is_approved:
#             self.is_approved = False
#             self.status = 'rejected'
#             self.save()
#
#     @property
#     def is_rejected(self):
#         return self.status == 'rejected'
#
#     @property
#     def total_leave_days_taken(self):
#         if self.startdate and self.enddate:
#             return (self.enddate - self.startdate).days
#         return 0
#
#     @property
#     def total_leave_days_remaining(self):
#         return self.total_leave_days_available - self.total_leave_days_taken
#
#
class CarriedForward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)  # Use ForeignKey to FinancialYear model
    leave_days_carried_forward = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(15)])

