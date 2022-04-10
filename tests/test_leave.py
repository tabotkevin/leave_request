import faker
from django.core.exceptions import ValidationError
from django.shortcuts import resolve_url
from django.test import TestCase

from leave import factories, models
from website.tests import AuthenticatedUserEnTestCase

fake = faker.Faker()


class LeaveRequestListPlVerificationTests(AuthenticatedUserEnTestCase):
    def test_status(self):
        factories.LeaveRequestFactory.create_batch(1)
        factories.LeaveRequestFactory.create_batch(
            1, status=models.LeaveRequestStatus.rejected
        )
        factories.LeaveRequestFactory.create_batch(
            1, status=models.LeaveRequestStatus.accepted
        )
        factories.LeaveRequestFactory.create_batch(
            1, status=models.LeaveRequestStatus.closed
        )
        url = resolve_url("leave:LeaveRequestList")
        response = self.client.get(url)
        self.assertContains(response, "open")
        self.assertContains(response, "rejected")
        self.assertContains(response, "accepted")
        self.assertContains(response, "closed")

    def test_no_none(self):
        factories.LeaveRequestFactory.create_batch(3)
        url = resolve_url("leave:LeaveRequestList")
        response = self.client.get(url)
        self.assertNotContains(response, "None")


class LeaveRequestVerificationTests(TestCase):
    def test_user_manager_cleanup(self):
        user = factories.UserFactory()
        manager = factories.UserFactory()
        item = factories.LeaveRequestFactory.build(request_by=user, manager=manager)
        self.assertRaises(ValidationError, item.clean)
