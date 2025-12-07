# inventariame/settings/production.py
import os
import dj_database_url
from .base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE, ROOT_URLCONF, TEMPLATES, WSGI_APPLICATION
from .base import AUTH_PASSWORD_VALIDATORS, LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ
from .base import STATIC_URL, STATICFILES_DIRS, STATIC_ROOT, DEFAULT_AUTO_FIELD
from .base import LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL, GOOGLE_MAPS_API_KEY

SECRET_KEY = os.getenv("SECRET_KEY", "inseguro-en-dev")
DEBUG = False
ALLOWED_HOSTS = ["inventariame-9bc51caf4b36.herokuapp.com"]

# Añadimos Whitenoise en producción
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
