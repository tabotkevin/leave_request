# -*- coding: utf-8 -*-
from enum import IntEnum

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# TODO: Use leave.models.User as a User model replacement for authentications
# TODO: Use 'user' and 'users' as display texts in Admin
# TODO: Make request timestamp set automatically
# TODO: Fill in all the user visible field and model names and descriptions


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=50, null=True, blank=True, unique=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    language = models.CharField(max_length=3, default="en")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username

    class Meta:
        default_related_name = "org_user"
        verbose_name = _('user')
        verbose_name_plural = _('users')


class LeaveRequestStatus(IntEnum):
    open = 0
    accepted = 1
    rejected = 2
    closed = 3


STATUSES = tuple((item.value, item.name) for item in list(LeaveRequestStatus))


class LeaveRequest(models.Model):
    start = models.DateField()
    end = models.DateField()
    request_by = models.ForeignKey(
        "leave.User", on_delete=models.CASCADE, related_name="days_off"
    )
    request_ts = models.DateTimeField(auto_now_add=True)
    # TODO: Make sure request wont be deleted by changes to the user table contents
    manager = models.ForeignKey(
        "leave.User", on_delete=models.PROTECT, related_name="requests"
    )
    status = models.PositiveSmallIntegerField(
        default=LeaveRequestStatus.open, choices=STATUSES
    )
    review_ts = models.DateTimeField(null=True, blank=True)

