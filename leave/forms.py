from django import forms
from django.utils.translation import gettext_lazy as _

from .models import LeaveRequest


class LeaveRequestForm(forms.ModelForm):
    
    class Meta:
        model = LeaveRequest
        fields = ['start', 'end']


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(LeaveRequestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        leave_request = super(LeaveRequestForm, self).save(commit=False)
        leave_request.request_by = self.user
        leave_request.manager = self.user.manager
        if commit:
            leave_request.save()
        return leave_request


class CreateLeaveRequestForm(LeaveRequestForm):
    pass


class UpdateLeaveRequestForm(LeaveRequestForm):
    pass


class ManagerUpdateLeaveRequestForm(forms.ModelForm):
    
    class Meta:
        model = LeaveRequest
        fields = ['status']
