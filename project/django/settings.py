from pathlib import Path
from project.settings.env import env
import os
import locale

BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = "django-insecure-@m$d^hbb#(**td8jk6730kk3njm_(hze#(slqujoh8imwc#^g%"

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(", ")

CORS_ALLOW_ALL_ORIGINS = True


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "transit_managment",
    "rest_framework",
    "drf_spectacular",
    "constance",
    "corsheaders",
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Street Router API",
    "DESCRIPTION": "API для построения маршрутов",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.django.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

if DEBUG:
    INSTALLED_APPS += ["silk"]
    MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]

WSGI_APPLICATION = "project.wsgi.application"


DATABASE_ENGINE = env("ENGINE", default="django.db.backends.sqlite3")

POSTGRES_DB = env("POSTGRES_DB", default="postgres")
POSTGRES_USER = env("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = env("POSTGRES_PASSWORD", default="postgres")
POSTGRES_HOST = env("POSTGRES_HOST", default="postgres")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)


if DATABASE_ENGINE == "django.db.backends.postgresql":
    try:
        import psycopg2

        connection = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
        )
        connection.close()

        DATABASES = {
            "default": {
                "ENGINE": DATABASE_ENGINE,
                "NAME": POSTGRES_DB,
                "USER": POSTGRES_USER,
                "PASSWORD": POSTGRES_PASSWORD,
                "HOST": POSTGRES_HOST,
                "PORT": POSTGRES_PORT,
            }
        }
    except (ImportError, psycopg2.OperationalError):
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


from project.settings.constance import *  # noqa: E402, F403
from project.settings.logging_config import *  # noqa: E402, F403
