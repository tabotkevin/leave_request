# -*- coding: utf-8 -*-
from enum import IntEnum

from django.contrib.auth.models import AbstractUser
from django.db import models

# TODO: Use leave.models.User as a User model replacement for authentications
# TODO: Use 'user' and 'users' as display texts in Admin
# TODO: Make request timestamp set automatically
# TODO: Fill in all the user visible field and model names and descriptions


class User(AbstractUser):
    manager = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    language = models.CharField(max_length=3, default="en")

    class Meta:
        default_related_name = "org_user"


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
    request_ts = models.DateTimeField()
    manager = models.ForeignKey(
        "leave.User", on_delete=models.CASCADE, related_name="requests"
    )
    status = models.PositiveSmallIntegerField(
        default=LeaveRequestStatus.open, choices=STATUSES
    )
    review_ts = models.DateTimeField(null=True, blank=True)

    # TODO: Make sure request wont be deleted by changes to the user table contents
