from django import forms

from .models import LeaveRequest


class LeaveRequestForm(forms.ModelForm):

    class Meta:
        model = LeaveRequest
        fields = ['start', 'end']


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        leave_request = super().save(commit=False)
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
