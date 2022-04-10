from __future__ import absolute_import, unicode_literals

from django import template

from leave.models import LeaveRequestStatus

register = template.Library()

@register.filter()
def to_str(value):
    return LeaveRequestStatus.get_status_name(value)
