"""
Django settings for emf_bus_tracking project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from django_query_profiler.settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = bool(os.getenv("DJANGO_DEBUG", False))

ALLOWED_HOSTS = ["tracking.tfemf.uk"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "celery",
    "colorfield",
    "corsheaders",
    "adminsortable2",
    "gtfs",
    "hafas",
    "kosmos",
    "darwin",
    "tracking",
]

if DEBUG:
    INSTALLED_APPS.append("django_query_profiler")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_cprofile_middleware.middleware.ProfilerMiddleware",
]

if DEBUG:
    MIDDLEWARE.append("django_query_profiler.client.middleware.QueryProfilerMiddleware")

ROOT_URLCONF = "emf_bus_tracking.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "emf_bus_tracking.wsgi.application"

DATABASES = {
    'default': {
        "ENGINE": "django_query_profiler.django.db.backends.postgresql"
        if DEBUG else "django.db.backends.postgresql",
        "HOST": os.getenv("DB_HOST", "localhost"),
        "NAME": os.getenv("DB_NAME", "emfta_tracking"),
        "USER": os.getenv("DB_USER", "emfta_tracking"),
        "PASSWORD": os.getenv("DB_PASS"),
    }
}

AUTH_PASSWORD_VALIDATORS = [{
    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
}, {
    "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
}, {
    "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
}, {
    "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
}]

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_RESULT_BACKEND = "rpc://"
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]

CELERY_BEAT_SCHEDULE = {
    "gtfs-rt": {
        "task": "gtfs.gtfs_rt_tasks.generate_gtfs_rt",
        "schedule": 10,
    },
    "kalman-estimate": {
        "task": "tracking.estimator.update_journey_estimates",
        "schedule": 15,
    }
}

TRANSIT_CONFIG = {
    "agency_id": "EMF",
    "agency_name": "Transport for EMF",
    "agency_url": "https://bus.emf.camp",
}

GTFS_CONFIG = {
    "agency": {
        "lang": "en",
        "phone": None,
        "fare_url": None,
        "email": "contact@emfcamp.org",
    },
    "feed": {
        "publisher": {
            "name": "Q Misell",
            "url": "https://magicalcodewit.ch",
        },
        "lang": "en",
        "contact_email": "q@magicalcodewit.ch",
        "contact_url": None,
    }
}

GTFS_TO_HTML_DATA_PATH = os.getenv("GTFS_TO_HTML_DATA_PATH")
GTFS_TO_HTML_OUTPUT_PATH = os.getenv("GTFS_TO_HTML_OUTPUT_PATH")
GTFS_TO_HTML_DOCKER = "theenbyperor/emf-gtfs-to-html:latest"

DATA_UPLOAD_MAX_NUMBER_FIELDS = None
DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400

OS_API_KEY = os.getenv("OS_API_KEY")

KOSMOS_TARGET_ID = os.getenv("KOSMOS_TARGET_ID")
KOSMOS_MAC_KEY = os.getenv("KOSMOS_MAC_KEY")

DARWIN_MESSAGING_HOST = os.getenv("DARWIN_MESSAGING_HOST")
DARWIN_MESSAGING_USERNAME = os.getenv("DARWIN_MESSAGING_USERNAME")
DARWIN_MESSAGING_PASSWORD = os.getenv("DARWIN_MESSAGING_PASSWORD")
DARWIN_CLIENT_ID = os.getenv("DARWIN_CLIENT_ID")
DARWIN_S3_ACCESS_KEY = os.getenv("DARWIN_S3_ACCESS_KEY")
DARWIN_S3_SECRET_KEY = os.getenv("DARWIN_S3_SECRET_KEY")

if DEBUG:
    DJANGO_QUERY_PROFILER_REDIS_HOST = os.getenv("DJANGO_QUERY_PROFILER_REDIS_HOST", "localhost")
    DJANGO_QUERY_PROFILER_REDIS_PORT = int(os.getenv("DJANGO_QUERY_PROFILER_REDIS_PORT", 6379))
    DJANGO_QUERY_PROFILER_REDIS_DB = int(os.getenv("DJANGO_QUERY_PROFILER_REDIS_DB", 0))


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": os.getenv("MEMCACHED_LOCATION", "localhost:11211"),
    }
}