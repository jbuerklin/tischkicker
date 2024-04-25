from .base import BASE_DIR

DEBUG = False

VITE_DEV_MODE = False
DJANGO_VITE_PLUGIN = {
    "DEV_MODE": VITE_DEV_MODE,
    "BUILD_DIR": BASE_DIR / "vite_build",
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# These need to be adjusted before deployment!
# Also have a look at this:
# https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
SECRET_KEY = ""
ALLOWED_HOSTS = []
STATIC_ROOT = ""
MEDIA_ROOT = ""
DATABASES = {}
DOMAIN = ""

# Also have a look at this:
# https://docs.djangoproject.com/en/4.2/ref/middleware/#http-strict-transport-security
SECURE_HSTS_SECONDS = 3600  # TODO: change to 31536000 if everything works
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
