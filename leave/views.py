# -*- coding: utf-8 -*-
# pylint: disable=too-many-ancestors

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from . import models

# TODO: Limit access to authenticated users


class LeaveRequestList(LoginRequiredMixin, ListView):
    template_name = "leave/LeaveRequest/list.html"
    model = models.LeaveRequest

    # TODO: Turn on pagination of 20 items per page


class LeaveRequestCreate(LoginRequiredMixin, CreateView):
    template_name = "leave/LeaveRequest/form.html"
    model = models.LeaveRequest
    fields = ("start", "end")

    # TODO: Setup user foreign keys from request
    # TODO: Setup success redirect to LeaveRequestDetail


class LeaveRequestDetail(LoginRequiredMixin, DetailView):
    template_name = "leave/LeaveRequest/detail.html"
    model = models.LeaveRequest

    # TODO: Allow manager to review this request by POST submit value of status=accepted/rejected
    # TODO: Validate submit value is in ('accepted', 'rejected') return HttpResponseBadRequest
    # TODO: Use translated "Please set correct status: {}" as response message
    # TODO: return HttpResponseForbidden if non manager tries to POST


class LeaveRequestUpdate(UserPassesTestMixin, UpdateView):
    template_name = "leave/LeaveRequest/form.html"
    model = models.LeaveRequest
    fields = ("start", "end")
    raise_exception = True

    # TODO: Redirect anonymous users to login
    # TODO: On successful update redirect to LeaveRequestDetail
    # TODO: Raise PermissionDenied for Users other than LeaveRequest.request_by
