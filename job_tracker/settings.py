"""
Django settings for the Job Application Tracker.
"""
import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # reads variables from a local .env file if present

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------- Core ----------
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-dev-key-change-me")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,jobflow-application-tracker.onrender.com"
    ).split(",")
    if h.strip()
]

# ---------- Applications ----------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tracker",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serves static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "job_tracker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,  # auto-discovers tracker/templates/tracker/*.html
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

WSGI_APPLICATION = "job_tracker.wsgi.application"

# ---------- Database ----------
# PostgreSQL configuration; DATABASE_URL is loaded from .env locally
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get(
            "DATABASE_URL",
            "postgresql://postgres:YOUR_PASSWORD@localhost:5432/job_tracker_db",
        ),
        conn_max_age=600,
    )
}

# ---------- Password validation ----------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------- Auth redirects ----------
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "board"
LOGOUT_REDIRECT_URL = "login"

# ---------- Internationalization ----------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ---------- Static files ----------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "tracker" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
