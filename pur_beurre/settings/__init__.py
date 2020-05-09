"""
Django settings for pur_beurre project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.urls import reverse_lazy

if os.environ.get('ENV') == 'PRODUCTION':
    import django_heroku


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)
)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nidgb+ve7tvhd7e^vj0vttx^!2a^5w@*l$5!o&&m7i*gz@a=mm'  # for dev

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('ENV') == 'PRODUCTION':
    DEBUG = False
else:
    DEBUG = True


if os.environ.get('ENV') == 'PRODUCTION':
    ALLOWED_HOSTS = ['purbeurre-etienne86.herokuapp.com']
else:
    ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_extensions',
    'off_sub',
    'auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'pur_beurre.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'off_sub.context_processors.pur_beurre_all_products',
                'off_sub.context_processors.pur_beurre_user_authenticated',

            ],
        },
    },
]

WSGI_APPLICATION = 'pur_beurre.wsgi.application'

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pur_beurre_db',
        'USER': 'ebarbier',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}

# Authentication
# User substitution
AUTH_USER_MODEL = 'my_auth.MyUser'
# Url for log in
LOGIN_URL = reverse_lazy('auth:sign')


# email params for dev
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

if os.environ.get('ENV') == 'PRODUCTION':
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.0/howto/static-files/
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if os.environ.get('ENV') == 'PRODUCTION':
    # Activate Django-Heroku
    django_heroku.settings(locals())
