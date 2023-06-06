"""
Django settings for cluster project.
Generated by 'django-admin startproject' using Django 3.2.8.
"""
import os
import environ

# # Set env vars, refer zeenote.md
env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get SECRET_KEY from env vars, use default if not found
SECRET_KEY = env("SECRET_KEY", default="django-insecure-91fugbgp0sndw1")

# Set DEBUG_VALUE from environment, default to false if not found
DEBUG = True

# Add localhost so local server command will also work
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # From here copied from allauth site
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "home",
    "music",
    "profiles",
    "checkout",
    "public",
    "crispy_forms",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ClusterSpotifyMusic.urls"

# Set crispy form template
CRISPY_TEMPLATE_PACK = "bootstrap4"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "allauth"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "music.context.project_context",  # Return project_context in music/context.py directly
            ],  # make its vars available in all pages without using their views
            "builtins": [
                "crispy_forms.templatetags.crispy_forms_tags",
                "crispy_forms.templatetags.crispy_forms_field",
            ],
        },
    },
]

# Note this is not required due to a default existing, but required for gitpod
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Line 1 - login by username in Django admin, regardless of `allauth`
# Line 2 - allauth specific authentication methods, such as login by e-mail
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# From allauth web
SITE_ID = 1

# Additional settings for allauth to work
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
AACOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGHT = 4
LOGIN_URL = "/accounts/login"  # Specify login url
LOGIN_REDIRECT_URL = "/"  # Redirect to site homepage after login

WSGI_APPLICATION = "ClusterSpotifyMusic.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Connect to postgres if DB_URL is set in env vars, otherwise
# use default sqlite. This allows loaddata & dumpdata commands to
# work after migrations to update remote db with existing data

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files directory (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Send confirmation email links to new user account at treminal
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Realtime confirmation email to register new user in live site
# if "DEVELOPMENT" in os.environ:
#     EMAIL_BACKEND = (
#         "django.core.mail.backends.console.EmailBackend"  # from default
#     )
#     DEFAULT_FROM_EMAIL = "example@clusterdomain.com"  # fake email sample
# else:
#     EMAIL_BACKEND = (
#         "django.core.mail.backends.smtp.EmailBackend"  # copied from gmail
#     )
#     EMAIL_USE_TLS = True
#     EMAIL_PORT = 587
#     EMAIL_HOST = "smtp.gmail.com"
#     EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
#     EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASS")
#     DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_HOST_USER")