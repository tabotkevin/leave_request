# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import RedirectView

from . import views as v

app_name = "leave"

urlpatterns = [
    url(r"^$", RedirectView.as_view(url="leave/list")),
    url(r"^leave/list$", v.LeaveRequestList.as_view(), name="LeaveRequestList"),
    url(r"^leave/create$", v.LeaveRequestCreate.as_view(), name="LeaveRequestCreate"),
    url(
        r"^leave/(?P<pk>[\d]+)/$",
        v.LeaveRequestDetail.as_view(),
        name="LeaveRequestDetail",
    ),
    url(
        r"^leave/(?P<pk>[\d]+)/update$",
        v.LeaveRequestUpdate.as_view(),
        name="LeaveRequestUpdate",
    ),
]
