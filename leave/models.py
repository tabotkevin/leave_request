# -*- coding: utf-8 -*-
from enum import IntEnum

from django.core.exceptions import ValidationError
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

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.username}"

    class Meta:
        default_related_name = "org_user"
        verbose_name = _('user')
        verbose_name_plural = _('users')


class LeaveRequestStatus(IntEnum):
    open = 0
    accepted = 1
    rejected = 2
    closed = 3

    @classmethod
    def get_status_name(cls, value):
        return {item.value: item.name for item in list(cls)}.get(value, 'open')

    @classmethod
    def get_status_value(cls, key):
        return {item.name: item.value for item in list(cls)}.get(key, 0)


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

    def clean(self):
        if (hasattr(self, 'request_by') and
                hasattr(self, 'manager') and
                self.request_by.manager != self.manager):
            message = 'Manager for this request must be user\'s manager '
            raise ValidationError(message)
        return super().clean()
