from django import test
from django.conf import settings
from django.shortcuts import resolve_url
from django.test import TestCase
from django.utils.translation import LANGUAGE_SESSION_KEY

from leave import factories


class AuthenticatedUserEnTestCase(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(manager=factories.UserFactory())
        self.client.force_login(self.user, settings.AUTHENTICATION_BACKENDS[0])
        session = self.client.session
        session.update({LANGUAGE_SESSION_KEY: "en"})
        session.save()


class AuthenticatedUserPlTestCase(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(manager=factories.UserFactory())
        self.client.force_login(self.user, settings.AUTHENTICATION_BACKENDS[0])
        session = self.client.session
        session.update({LANGUAGE_SESSION_KEY: "pl"})
        session.save()


class SuperUserEnTestCase(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(
            email="foo@bar.com", is_superuser=True, is_staff=True, is_active=True
        )
        self.user.save()
        self.client.force_login(self.user, settings.AUTHENTICATION_BACKENDS[0])
        session = self.client.session
        session.update({LANGUAGE_SESSION_KEY: "en"})
        session.save()


class SuperUserPlTestCase(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(
            email="foo@bar.com", is_superuser=True, is_staff=True, is_active=True
        )
        self.user.save()
        self.client.force_login(self.user, settings.AUTHENTICATION_BACKENDS[0])
        session = self.client.session
        session.update({LANGUAGE_SESSION_KEY: "pl"})
        session.save()


class TestAdminAvailable(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(
            email="foo@bar.com", is_superuser=False, is_staff=True, is_active=True
        )
        self.user.save()
        self.client.force_login(self.user, settings.AUTHENTICATION_BACKENDS[0])

    def test_admin_get(self):
        url = resolve_url("admin:index")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
