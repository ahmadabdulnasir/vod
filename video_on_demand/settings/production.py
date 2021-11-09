from google.oauth2 import service_account
from .base import *
from .dbconf import POSTGRESDB, MANGODB

"""Production Ready Settings
"""

TEMP_SECRET_KEY = "srt@v69cp$hm2^g-z#m%n18pl(+*mmx6+tl$t^s9h55%1v%*it"
SECRET_KEY = os.environ.get("SECRET_KEY", TEMP_SECRET_KEY)
DEBUG = False

ALLOWED_HOSTS += [
    "vod.edu.ng",
    "www.vod.edu.ng",
    "vod.dabolinux.com",
    "www.vod.dabolinuxcom",
    "backend.arewacinema.com",
    "www.backend.arewacinema.com",
    "api.arewacinema.com",
    "www.api.arewacinema.com",
    "vod.com.ng",
    "www.vod.com.ng",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

DATABASES = POSTGRESDB
# DATABASES = MANGODB


STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")
STATIC_URL = "/vodstatic/"
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static"),)
MEDIA_URL = "/vodmedia/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")


# Google cloud for images
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_PROJECT_ID = 'arewacinema'
GS_BUCKET_NAME = 'arewacinema_bucket'
GS_FILE_OVERWRITE = True
GS_LOCATION = 'arewacinema/vod'
GS_AUTH_FILE = os.path.join(PROJECT_ROOT, "arewacinema-65696f642f71.json")
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    GS_AUTH_FILE)
