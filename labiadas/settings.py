"""
Django settings for labiadas project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+*w1wm^xq*3u8pybmcd*+w!vnk+wt%_y^m64os@i3a(i74#yp#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0',
                 '79.137.39.201']


STATIC_ROOT = os.path.join(BASE_DIR, "romani/static/")

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'geoposition',
    'captcha',
    'notifications',
    'django_messages',
    'romani',
)

SITE_ID = 1


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'labiadas.urls'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'django_messages.context_processors.inbox',
                'labiadas.context_processors.notifications_user',
            ],
        },
    },
]

WSGI_APPLICATION = 'labiadas.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'romani/templates'),
)


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


LOCALE_PATHS = ( "locale/",)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-ca'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

gettext = lambda s: s
LANGUAGES = (
    ('es-ca', gettext('Catalan')),
    # ('es-es', gettext('Spanish')),
)



TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, 'static').replace('\\','/'),]



SEND_EMAIL = True
ACCOUNT_ACTIVATION_DAYS = 30
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'scaladeirsvc@gmail.com'
EMAIL_HOST_PASSWORD = 'ppcefdwfayrhrwrb'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

from django.core.urlresolvers import reverse_lazy
LOGIN_URL=reverse_lazy("login")
LOGIN_REDIRECT_URL=reverse_lazy("coope")
LOGOUT_URL=reverse_lazy("coope")
# REGISTRATION_OPEN = False


GEOPOSITION_GOOGLE_MAPS_API_KEY = ' AIzaSyA6f7rjDkdoQZFH3uy9UTOF7r8xxyOTAcE '

AUTHENTICATION_BACKENDS = (
    'romani.models.EmailModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)
