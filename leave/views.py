
# -*- coding: utf-8 -*-
# pylint: disable=too-many-ancestors

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CreateLeaveRequestForm, ManagerUpdateLeaveRequestForm, UpdateLeaveRequestForm
from .models import LeaveRequest, LeaveRequestStatus


# TODO: Limit access to authenticated users
class LeaveRequestList(LoginRequiredMixin, ListView):
    template_name = "leave/LeaveRequest/list.html"
    model = LeaveRequest
    # TODO: Turn on pagination of 20 items per page
    paginate_by = 20
    ordering = ['-id']


class LeaveRequestCreate(LoginRequiredMixin, CreateView):
    template_name = "leave/LeaveRequest/form.html"
    model = LeaveRequest
    form_class = CreateLeaveRequestForm
    success_message = _('Leave Request created.')

    # TODO: Setup user foreign keys from request
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # TODO: Setup success redirect to LeaveRequestDetail
    def get_success_url(self):
        return reverse('leave:LeaveRequestDetail', kwargs=dict(pk=self.object.pk))



class LeaveRequestDetail(LoginRequiredMixin, DetailView):
    template_name = "leave/LeaveRequest/detail.html"
    model = LeaveRequest

    def test_func(self):
        leave_request = self.get_object()
        return leave_request.request_by == self.request.user.manager

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ManagerUpdateLeaveRequestForm
        return context

    # TODO: Allow manager to review this request by POST submit value of status=accepted/rejected
    def post(self, request, *args, **kwargs):  #pylint: disable=unused-argument

        # TODO: return HttpResponseForbidden if non manager tries to POST
        if self.request.user != self.get_object().manager:
            return HttpResponseForbidden()

        form = ManagerUpdateLeaveRequestForm(request.POST)

        status = request.POST.get('status')
        if not status in ('accepted', 'rejected'):
            # TODO: Use translated "Please set correct status: {}" as response message
            message = _(f"Please set correct status: {status}")
            # TODO: Validate submit value is in ('accepted', 'rejected') return HttpResponseBadRequest
            return HttpResponseBadRequest(message)

        self.object = self.get_object()
        self.object.status = LeaveRequestStatus.get_status_value(status)
        self.object.review_ts = timezone.now()
        self.object.save()
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return HttpResponseRedirect(reverse("leave:LeaveRequestList"))


class LeaveRequestUpdate(UserPassesTestMixin, UpdateView):
    template_name = "leave/LeaveRequest/form.html"
    model = LeaveRequest
    form_class = UpdateLeaveRequestForm
    raise_exception = True
    success_message = _('Leave Request Updated.')

    # TODO: Raise PermissionDenied for Users other than LeaveRequest.request_by
    def test_func(self):
        leave_request = self.get_object()
        return leave_request.request_by == self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # TODO: On successful update redirect to LeaveRequestDetail
    def get_success_url(self):
        return reverse('leave:LeaveRequestDetail', kwargs=dict(pk=self.get_object().pk))

    # TODO: Redirect anonymous users to login
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
