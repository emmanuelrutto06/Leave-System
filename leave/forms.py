from django import forms
from .models import Leave
import datetime

class LeaveCreationForm(forms.ModelForm):
    reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

    class Meta:
        model = Leave
        exclude = ['status', 'user', 'is_approved', 'updated', 'created', 'default_leave_days', 'leave_days_taken', 'leave_days_remaining', 'default_annual_leave_days', 'total_leave_days_available']
        # 'user', 'defaultdays', 'hrcomments', 


    def clean_enddate(self):
        enddate = self.cleaned_data['enddate']
        startdate = self.cleaned_data['startdate']
        today_date = datetime.date.today()

        if (startdate or enddate) < today_date:  # both dates must not be in the past
            raise forms.ValidationError("Selected dates are incorrect,please select again")

        elif startdate >= enddate:  # TRUE -> FUTURE DATE > PAST DATE,FALSE other wise
            raise forms.ValidationError("Selected dates are wrong")

        return enddate
