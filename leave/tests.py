import logging

import faker
from django import test
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import resolve_url

from website.tests import (
    AuthenticatedUserEnTestCase,
    AuthenticatedUserPlTestCase,
    SuperUserEnTestCase,
    SuperUserPlTestCase,
)

from . import factories, models

log = logging.getLogger(__name__)
fake = faker.Faker()


class LeaveRequestCreateTests(AuthenticatedUserEnTestCase):
    def test_anonymous(self):
        url = resolve_url("leave:LeaveRequestCreate")
        response = test.Client().get(url)
        self.assertEqual(302, response.status_code)

    def test_get(self):
        url = resolve_url("leave:LeaveRequestCreate")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_post(self):
        url = resolve_url("leave:LeaveRequestCreate")
        start = fake.future_date()
        end = fake.future_date()
        response = self.client.post(url, data={"start": start, "end": end})
        item = models.LeaveRequest.objects.first()
        self.assertEqual(start, item.start)
        self.assertEqual(end, item.end)
        self.assertEqual(self.user.manager, item.manager)
        self.assertEqual(self.user, item.request_by)
        self.assertRedirects(response, resolve_url("leave:LeaveRequestDetail", item.pk))


class LeaveRequestUpdateTests(AuthenticatedUserEnTestCase):
    def test_anonymous(self):
        item = factories.LeaveRequestFactory()
        url = resolve_url("leave:LeaveRequestUpdate", item.pk)
        response = test.Client().get(url)
        self.assertEqual(302, response.status_code)

    def test_forbidden(self):
        item = factories.LeaveRequestFactory()
        url = resolve_url("leave:LeaveRequestUpdate", item.pk)
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)

    def test_get(self):
        item = factories.LeaveRequestFactory(request_by=self.user)
        url = resolve_url("leave:LeaveRequestUpdate", item.pk)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_post(self):
        item = factories.LeaveRequestFactory(
            request_by=self.user, manager=self.user.manager
        )
        url = resolve_url("leave:LeaveRequestUpdate", item.pk)
        start = fake.future_date()
        end = fake.future_date()
        response = self.client.post(url, data={"start": start, "end": end})
        item.refresh_from_db()
        self.assertEqual(start, item.start)
        self.assertEqual(end, item.end)
        self.assertEqual(self.user.manager, item.manager)
        self.assertEqual(self.user, item.request_by)
        self.assertRedirects(response, resolve_url("leave:LeaveRequestDetail", item.pk))


class LeaveRequestDetailEnTests(AuthenticatedUserEnTestCase):
    def test_400_bad(self):
        item = factories.LeaveRequestFactory(manager=self.user)
        url = resolve_url("leave:LeaveRequestDetail", item.pk)
        response = self.client.post(url, data={"status": "bad"})
        self.assertEqual(400, response.status_code)
        self.assertEqual(b"Please set correct status: bad", response.content)
        item.refresh_from_db()
        self.assertEqual(models.LeaveRequestStatus.open, item.status)
        self.assertIsNone(item.review_ts)

    def test_400_missing(self):
        item = factories.LeaveRequestFactory(manager=self.user)
        url = resolve_url("leave:LeaveRequestDetail", item.pk)
        response = self.client.post(url)
        self.assertEqual(400, response.status_code)
        self.assertEqual(b"Please set correct status: None", response.content)
        item.refresh_from_db()
        self.assertEqual(models.LeaveRequestStatus.open, item.status)
        self.assertIsNone(item.review_ts)

    def test_accept(self):
        item = factories.LeaveRequestFactory(manager=self.user)
        url = resolve_url("leave:LeaveRequestDetail", item.pk)
        response = self.client.post(url, data={"status": "accepted"})
        self.assertRedirects(response, resolve_url("leave:LeaveRequestList"))
        item.refresh_from_db()
        self.assertEqual(models.LeaveRequestStatus.accepted, item.status)
        self.assertIsNotNone(item.review_ts)

    def test_reject(self):
        item = factories.LeaveRequestFactory(manager=self.user)
        url = resolve_url("leave:LeaveRequestDetail", item.pk)
        response = self.client.post(url, data={"status": "rejected"})
        self.assertRedirects(response, resolve_url("leave:LeaveRequestList"))
        item.refresh_from_db()
        self.assertEqual(models.LeaveRequestStatus.rejected, item.status)
        self.assertIsNotNone(item.review_ts)

    def test_no_none(self):
        item = factories.LeaveRequestFactory(manager=self.user)
        url = resolve_url("leave:LeaveRequestDetail", item.pk)
        response = self.client.get(url)
        self.assertNotContains(response, "None")

    def test_status(self):
        item = factories.LeaveRequestFactory(manager=self.user)
        url = resolve_url("leave:LeaveRequestDetail", item.pk)
        response = self.client.get(url)
        self.assertContains(response, "open")


class LeaveRequestListTests(AuthenticatedUserPlTestCase):
    def test_anonymous(self):
        url = resolve_url("leave:LeaveRequestList")
        response = test.Client().get(url)
        self.assertEqual(302, response.status_code)

    def test_get(self):
        factories.LeaveRequestFactory.create_batch(21)
        url = resolve_url("leave:LeaveRequestList")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(20, len(response.context_data["object_list"]))
        self.assertEqual(20, response.context_data["paginator"].per_page)


class UserAdminPlTests(SuperUserPlTestCase):
    def test_admin_get(self):
        url = resolve_url("admin:index")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Użytkownicy")

    def test_laguages(self):
        factories.UserFactory(language="pl")
        factories.UserFactory(language="en")
        factories.UserFactory(language="XXX")
        url = resolve_url(admin_urlname(models.User._meta, "changelist"))
        response = self.client.get(url)
        self.assertContains(response, "pl")
        self.assertContains(response, "en")
        self.assertContains(response, "XXX")

    def test_manager(self):
        item = factories.UserFactory(language="pl", manager=factories.UserFactory())
        url = resolve_url(admin_urlname(models.User._meta, "changelist"))
        response = self.client.get(url)
        self.assertContains(response, item.manager.username)


class UserAdminEnTests(SuperUserEnTestCase):
    def test_admin_get(self):
        url = resolve_url("admin:index")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Users")
