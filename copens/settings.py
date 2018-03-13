# -*- coding: utf-8 -*-
import os
import glob

from registration_defaults.settings import REGISTRATION_TEMPLATE_DIR

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'b^t*u5vhgwcrw-q9dy0tqo^^_l@#32=#17ss2^t0wt@a7yg#&9'

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

SITE_ID = 1

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = "25"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = "copens <copens@lopen.linguistics.ntu.edu.tw>"

LOGIN_REDIRECT_URL = 'http://lopen.linguistics.ntu.edu.tw/copens/'

INSTALLED_APPS = (
    'control_panel',
    'api',
    'rest_framework',
    'rest_framework.authtoken',
    'django_pygments',
    'django_facebook',
    'about',
    'misc',
    'wordlist',
    'copenAuth',
    'captcha',
    'endless_pagination',
    'registration_custom',
    'registration_defaults',
    'cwm',
    'brat',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

ACCOUNT_ACTIVATION_DAYS = 2

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'copens.urls'

WSGI_APPLICATION = 'copens.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static_cwm/'
STATICFILES_DIRS = (os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'static'), )
STATIC_ROOT = os.path.join(BASE_DIR, 'static_all')


TEMPLATE_DIRS = (
    REGISTRATION_TEMPLATE_DIR,
    os.path.join(BASE_DIR, 'registration_defaults/templates/registration'
                 ),  # --> this will override the above path
)

TEMPLATE_DIRS += tuple(glob.glob(os.path.join(BASE_DIR, 'templates/*')))

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'cwm.context_processors.include_search_form',
    'django.contrib.auth.context_processors.auth',
    'django_facebook.context_processors.facebook',
)

AUTHENTICATION_BACKENDS = (
    'django_facebook.auth_backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SESSION_COOKIE_AGE = 365 * 24 * 60 * 600

ENDLESS_PAGINATION_PER_PAGE = 100

LOGIN_URL = '/login/'

UPLOAD_FILE_DIRS = os.path.join(BASE_DIR, 'upload_files')

FACEBOOK_APP_ID = os.environ['fb_app_id'] 
FACEBOOK_APP_SECRET = os.environ['fb_app_secret'] 

AUTH_PROFILE_MODULE = 'django_facebook.FacebookProfile'
FACEBOOK_LOGIN_DEFAULT_REDIRECT = '/copens'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':
    ('rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_THROTTLE_CLASSES': ('rest_framework.throttling.AnonRateThrottle',
                                 'rest_framework.throttling.UserRateThrottle'),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '30/minute'
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log', 'debug.log'),
        },
    },
    'loggers': {
        'cwm': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}
