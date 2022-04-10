# -*- coding: utf-8
from __future__ import absolute_import

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LeaveConfig(AppConfig):
    name = "leave"
    verbose_name = _("Django Leave Basic Test")
