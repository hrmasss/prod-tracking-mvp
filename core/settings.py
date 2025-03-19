import os
import dj_database_url
from pathlib import Path
from logging import getLogger
from datetime import timedelta
from dotenv import load_dotenv
from common.unfold import UNFOLD_CONFIG
from django.core.management.utils import get_random_secret_key


# --- LOGGER ---
log = getLogger(__name__)

# --- BASE DIRECTORY ---
# Base directory to simplify path configurations
BASE_DIR = Path(__file__).resolve().parent.parent

# --- ENVIRONMENT VARIABLES ---
# Environment variables from the .env file
load_dotenv(BASE_DIR / ".env")

# --- SECRET KEY ---
# Secret key from the environment; generate a random one if not set
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    log.warning(
        "SECRET_KEY is not set; generating a random one, do not use in production!"
    )
    SECRET_KEY = get_random_secret_key()

# --- DEBUG ---
# Debug mode based on the environment variable
DEBUG = os.getenv("DEBUG", "False") == "True"
if DEBUG:
    log.warning("DEBUG is set to True; this should not be used in production!")

# --- ALLOWED HOSTS ---
# Allowed hosts for the application
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

# --- APPLICATION DEFINITIONS ---
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.simple_history",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party applications
    "corsheaders",
    "simple_history",
    "safedelete",
    "guardian",
    "auditlog",
    "django_extensions",
    # Local applications
    "common",
    "users",
    "tracker",
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

# --- ROOT URL CONFIGURATION ---
ROOT_URLCONF = "core.urls"

# --- TEMPLATES ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# --- WSGI APPLICATION ---
WSGI_APPLICATION = "core.wsgi.application"

# --- STATIC AND MEDIA URLS ---
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# --- STATIC AND MEDIA ROOTS ---
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"

# --- DATABASE CONFIGURATION ---
# Use SQLite if no database URL is provided
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600),
}

# --- AUTH USER MODEL ---
AUTH_USER_MODEL = "users.User"

# --- AUTHENTICATION BACKENDS ---
AUTHENTICATION_BACKENDS = (
    "users.backends.EmailOrUsernameModelBackend",
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

# --- PASSWORD VALIDATORS ---
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

# --- CORS CONFIGURATION ---
CORS_ALLOW_CREDENTIALS = True
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    ALLOWED_HOSTS = ["*"]
else:
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = "en-us"
USE_I18N = True

# --- TIME ZONE ---
TIME_ZONE = "Asia/Dhaka"
USE_TZ = True

# --- DEFAULT AUTO FIELD ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- EMAIL CONFIGURATION ---
EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
    if not DEBUG
    else "django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT", 587)
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# --- LOGGING CONFIGURATION ---
# Logging configuration for both development and production environments

# Ensure the logs directory exists
log_dir = BASE_DIR / "logs"
log_file_path = log_dir / "django.log"
os.makedirs(log_dir, exist_ok=True)

# Ensure the log file exists
if not log_file_path.exists():
    log_file_path.touch()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "simple",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": str(log_file_path),
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
}

# --- TEST RUNNER ---
TEST_RUNNER = "pytest_runner.runner.PytestTestRunner"

# --- NINJA JWT CONFIGURATION ---
NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}

# --- UNFOLD CONFIGURATION ---
UNFOLD = UNFOLD_CONFIG
