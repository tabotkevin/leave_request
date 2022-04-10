import os
import re
import socket
from pathlib import Path

import pycountry

# Project root folder
BASE_DIR = Path(__file__).parents[1]

# This is defined here as a do-nothing function because we can't import
# django.utils.translation -- that module depends on the settings.
# https://docs.djangoproject.com/en/1.9/topics/i18n/translation/#marking-strings-as-no-op
gettext_noop = lambda s: s  # noqa: E731

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", True))
ENVIRONMENT_NAME = os.environ.get("ENVIRONMENT_NAME", default="")

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", default="no-secret")
INTERNAL_IPS = ["127.0.0.1"]

ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".example.com", "vagrant"]

BASE_DOMAIN = HOSTNAME = socket.gethostname().lower()
if "ALLOWED_HOSTS" in os.environ and os.environ["ALLOWED_HOSTS"].strip():
    hosts = os.environ["ALLOWED_HOSTS"].split(" ")
    ALLOWED_HOSTS = [host.strip() for host in hosts if host.strip()]

BASE_URL = os.environ.get("BASE_URL", default="http://127.0.0.1:8000")

SECURE_SSL_REDIRECT = bool(os.environ.get("SECURE_SSL_REDIRECT", default=False))

ADMINS = (
    ("Administrator", "{domain} admin <admin@{domain}>".format(domain=BASE_DOMAIN)),
)
if "ADMINS" in os.environ:
    from email.utils import getaddresses

    admins = os.environ["ADMINS"].split(";")
    addreses = getaddresses(admins)
    ADMINS = [
        (name, named_email) for ((name, email), named_email) in zip(addreses, admins)
    ]

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", default="Help <help@{domain}>".format(domain=BASE_DOMAIN)
)
HELP_EMAIL = os.environ.get("HELP_EMAIL", default=DEFAULT_FROM_EMAIL)
ERR_EMAIL = os.environ.get(
    "ERR_EMAIL", default="errors@{domain}".format(domain=BASE_DOMAIN)
)
SERVER_EMAIL = os.environ.get(
    "SERVER_EMAIL", default="Errors <errors@{domain}>".format(domain=BASE_DOMAIN)
)
EMAIL_SUBJECT_PREFIX = os.environ.get("EMAIL_SUBJECT_PREFIX", default="[DJANGO] ")

# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # nose wants it
    "leave.apps.LeaveConfig",
)

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "website.urls"

TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/1.8/topics/templates/#django.template.backends.django.DjangoTemplates
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    }
]

WSGI_APPLICATION = "website.wsgi.application"

FIXTURE_DIRS = [str(BASE_DIR / "fixtures")]

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "data" / "db.dev.sqlite3"),
        "TEST": {"NAME": ":memory:"},
    }
}

# The email backend to use. For possible shortcuts see django.core.mail.
# The default is to use the SMTP backend.
# Third-party backends can be specified by providing a Python path
# to a module that defines an EmailBackend class.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = "en"
LANGUAGES = (("en", gettext_noop("English")), ("pl", gettext_noop("Polish")))
TIME_ZONE = "Europe/Warsaw"
USE_I18N = True

LOCALE_PATHS = [
    str(BASE_DIR / "locale"),
    str(Path(pycountry.__file__).parent / "locales"),
]

USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = BASE_URL + "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "media")
STATIC_ROOT = str(BASE_DIR / "static")

# The default file storage backend used during the build process
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

IGNORABLE_404_URLS = (
    re.compile(r"\.(php|cgi)$"),
    re.compile(r"^/admin/"),
    re.compile(r"^/phpmyadmin/"),
)

# django-guardian
# http://django-guardian.readthedocs.org/en/v1.2/configuration.html

ANONYMOUS_USER_ID = -1

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # this is default
)

LOGIN_REDIRECT_URL = "/"

# https://docs.djangoproject.com/en/1.9/ref/settings/#logging
LOGGING = {
    "version": 1,
    # Setting this to True will disable for eg. preexisting Celery loggers
    "disable_existing_loggers": False,
    "formatters": {
        "short": {
            "format": "%(asctime)s %(levelname)-7s %(thread)-5d %(message)s",
            "datefmt": "%H:%M:%S",
        },
        # this may slow down the app a little, due to
        "verbose": {
            "format": "%(asctime)s %(levelname)-7s %(thread)-5d %(name)s %(filename)s:%(lineno)s | %(funcName)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "heroku": {
            "format": "%(levelname)-7s %(thread)-5d %(name)s %(filename)s:%(lineno)s | %(funcName)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "short",
            "level": "DEBUG",
        },
        "mail_admins": {
            "level": "ERROR",
            "email_backend": "django.core.mail.backends.smtp.EmailBackend",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django.template": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {"handlers": ["console"], "propagate": False, "level": "INFO"},
        "django.security.DisallowedHost": {"handlers": [], "propagate": False},
        "suds": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "django.db.backends": {
            "handlers": ["console"],
            "propagate": True,
            "level": "WARNING",
        },
        "factory.generate": {
            "handlers": ["console"],
            "propagate": True,
            "level": "WARNING",
        },
        "factory.containers": {
            "handlers": ["console"],
            "propagate": True,
            "level": "WARNING",
        },
        "dinja2": {"handlers": ["console"], "propagate": True, "level": "WARNING"},
        "raven": {"level": "INFO", "handlers": ["console"], "propagate": False},
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
