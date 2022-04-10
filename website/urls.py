"""website URL Configuration"""
from django.conf.urls import include, url
from django.contrib import admin

sitemaps = {}

urlpatterns = [
    url(r"admin/", admin.site.urls),
    url(r"i18n/", include("django.conf.urls.i18n")),
    url(r"accounts/", include("django.contrib.auth.urls")),
    url(r"", include("leave.urls")),
]
