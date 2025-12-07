# inventariame/settings/development.py
from .base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE, ROOT_URLCONF, TEMPLATES, WSGI_APPLICATION
from .base import AUTH_PASSWORD_VALIDATORS, LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ
from .base import STATIC_URL, STATICFILES_DIRS, STATIC_ROOT, DEFAULT_AUTO_FIELD
from .base import LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL, GOOGLE_MAPS_API_KEY

SECRET_KEY = "django-insecure-lish1rv^5yi%v8)y53mg*cdz@1#6!af+yrzh62#m)*s0%ae9#$"
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
