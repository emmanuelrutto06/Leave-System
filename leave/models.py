from django.db import models
from .manager import LeaveManager
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from datetime import date

ANNUAL = 'annual'
SICK = 'sick'
# CASUAL = 'casual'
# EMERGENCY = 'emergency'
# STUDY = 'study'
# MATERNITY = 'maternity'
# BEREAVEMENT = 'bereavement'
# QUARANTINE = 'quarantine'
# COMPENSATORY = 'compensatory'
# SABBATICAL = 'sabbatical'

LEAVE_TYPE = (
    (ANNUAL, 'annual'),
    (SICK, 'Sick Leave'),
    # (CASUAL, 'Casual Leave'),
    # (EMERGENCY, 'Emergency Leave'),
    # (STUDY, 'Study Leave'),
    # (MATERNITY, 'Maternity Leave'),
    # (BEREAVEMENT, 'Bereavement Leave'),
    # (QUARANTINE, 'Self Quarantine'),
    # (COMPENSATORY, 'Compensatory Leave'),
    # (SABBATICAL, 'Sabbatical Leave')
)



class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    startdate = models.DateField(verbose_name=_('Start Date'), help_text='leave start date is on ..', null=True, blank=False)
    enddate = models.DateField(verbose_name=_('End Date'), help_text='coming back on ...', null=True, blank=False)
    leavetype = models.CharField(choices=LEAVE_TYPE, max_length=25, default=SICK, null=True, blank=False)
    reason = models.CharField(verbose_name=_('Reason for Leave'), max_length=255, help_text='add additional information for leave', null=True, blank=True)
    default_leave_days = models.PositiveIntegerField(default=30)
    leave_days_taken = models.PositiveIntegerField(default=0)
    leave_days_remaining = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=12, default='pending')
    is_approved = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    objects = LeaveManager()

    
    class Meta:
        verbose_name = _('Leave')
        verbose_name_plural = _('Leaves')
        ordering = ['-created']
                
    def __str__(self):
        return '{0} - {1}'.format(self.leavetype, self.user)

    @property
    def pretty_leave(self):
        '''
        i don't like the __str__ of leave object - this is a pretty one :-)
        '''
        leave = self.leavetype
        user = self.user
        employee = user.employee_set.first().get_full_name
        return '{0} - {1}'.format(employee, leave)

    @property
    def leave_approved(self):
        return self.is_approved == True
    
    @property
    def approve_leave(self):
        if not self.is_approved:
            self.is_approved = True
            self.status = 'approved'
            self.save()
    
    @property
    def unapprove_leave(self):
        if self.is_approved:
            self.is_approved = False
            self.status = 'pending'
            self.save()

    @property
    def leaves_cancel(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'cancelled'
            self.save()

    @property
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
            return (self.enddate - self.startdate).days + 1
        return 0

    @property
    def total_leave_days_remaining(self):
        return self.default_leave_days - self.total_leave_days_taken
    print(total_leave_days_remaining)


# Create an instance of LeaveModel
leave = Leave(
    startdate=date(2023, 6, 17),
    enddate=date(2023, 6, 29),
)
 
leave.save()

context = {
    'leave': leave,
}
# Access the leave days taken and remaining
default_leave_days = leave.default_leave_days
days_taken = leave.total_leave_days_taken
days_remaining = leave.total_leave_days_remaining

print("total leave days:", default_leave_days)
print("Days taken:", days_taken)
print("Days remaining:", days_remaining)