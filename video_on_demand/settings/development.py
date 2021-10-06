from .base import *
from .dbconf import POSTGRESDB, DEVELOPMENTDB

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)1qj5yvc+8zx5wdx1^+k5&jsb7l!sjqz+u4%ti%=d((u#cqp_5"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS += ["*"]

# Database
DATABASES = DEVELOPMENTDB


STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")
STATIC_URL = "/vodstatic/"
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static"), "static")
MEDIA_URL = "/vodmedia/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
