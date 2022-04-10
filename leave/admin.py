# coding=utf-8

import logging

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import LeaveRequest, User

log = logging.getLogger(__name__)

# TODO: Add user admin for models.User
# TODO: Make sure text translations remain in place
# TODO: Show language and manager in list table columns

@admin.register(User)
class UsersAdmin(UserAdmin):
    list_display = ('manager', 'language')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('start', 'end', 'request_by', 'request_ts', 'manager', 'status')
