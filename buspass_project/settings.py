"""
Django settings for buspass_project project.
"""

from pathlib import Path
import os
import dj_database_url

# ===============================
# BASE DIRECTORY
# ===============================

BASE_DIR = Path(__file__).resolve().parent.parent


# ===============================
# SECURITY SETTINGS
# ===============================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-local-dev-key'
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    '127.0.0.1,localhost,digital-buss-pass.onrender.com'
).split(',')

AUTH_USER_MODEL = 'accounts.CustomUser'


# ===============================
# INSTALLED APPS
# ===============================

INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',

    # Project Apps
    'accounts',
    'students',
    'adminpanel',
    'payments',
    'verification',
    'notifications',
    'reports',
]


# ===============================
# MIDDLEWARE
# ===============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Static files support
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ===============================
# ROOT URL CONFIG
# ===============================

ROOT_URLCONF = 'buspass_project.urls'


# ===============================
# TEMPLATES
# ===============================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ===============================
# WSGI APPLICATION
# ===============================

WSGI_APPLICATION = 'buspass_project.wsgi.application'


# ===============================
# DATABASE CONFIG
# ===============================

if os.environ.get("DATABASE_URL"):
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ.get("DATABASE_URL")
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ===============================
# PASSWORD VALIDATION
# ===============================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ===============================
# INTERNATIONALIZATION
# ===============================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# ===============================
# STATIC FILES
# ===============================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# ===============================
# MEDIA FILES
# ===============================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"


# ===============================
# CRISPY FORMS
# ===============================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# ===============================
# DEFAULT PRIMARY KEY FIELD
# ===============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'