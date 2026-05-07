import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "animalerie-dev-secret"
DEBUG = True
ALLOWED_HOSTS = ["*"]
CATS_API_URL = os.getenv("CATS_API_URL", "http://host.docker.internal:8002/api/cats/")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "host.docker.internal",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "adoptions",
    "fournisseurs",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "animalerie_config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "animalerie_config.wsgi.application"
ASGI_APPLICATION = "animalerie_config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "animalerie_db"),
        "USER": os.environ.get("POSTGRES_USER", "animalerie"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "animalerie"),
        "HOST": os.environ.get("POSTGRES_HOST", "animalerie_db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ELEVAGE_API_BASE_URL = os.environ.get("ELEVAGE_API_BASE_URL", "http://localhost:8000")
