import os
from decouple import config
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key
SECRET_KEY = os.environ.get("SECRET_KEY", "your-default-secret-key")

# Debug mode
DEBUG = False  # os.environ.get("DEBUG", "False") == "True"

# Allowed hosts
ALLOWED_HOSTS = [
    "8000-owuradaps-flavourfusion-8hkcnr8a5lb.ws.codeinstitute-ide.net",
    ".herokuapp.com",
]

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "account",
    "recipe",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# URL configuration
ROOT_URLCONF = "flavourfusion-pro.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

# WSGI application
WSGI_APPLICATION = "flavourfusion-pro.wsgi.application"

# # Database configuration
# DATABASES = {
#     "default": dj_database_url.config(
#         default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
#     )
# }

# Database configuration
DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}


CSRF_TRUSTED_ORIGINS = [
    "https://8000-owuradaps-flavourfusion-8hkcnr8a5lb.ws.codeinstitute-ide.net",
    "https://*.herokuapp.com",
]

# Password validation
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

# Localization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
}

# Other settings
DATABASES = {"default": dj_database_url.config(default=config("DATABASE_URL"))}

SECRET_KEY = config("SECRET_KEY")
DEBUG = False  # Ensure DEBUG is False in production
ALLOWED_HOSTS = [".herokuapp.com", "your_custom_domain.com"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
