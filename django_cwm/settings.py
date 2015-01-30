# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from settings_conf import *
import os, glob
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

SITE_ID = 1

LOGIN_REDIRECT_URL = 'home'

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

ROOT_URLCONF = 'django_cwm.urls'

WSGI_APPLICATION = 'django_cwm.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static_cwm/'
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)),'static'),
)

from registration_defaults.settings import *

#TEMPLATE PATH
TEMPLATE_DIRS = (
    REGISTRATION_TEMPLATE_DIR,
    os.path.join(BASE_DIR, 'registration_defaults/templates/registration'), # --> this will override the above path
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

#Django-endless-pagination settings
ENDLESS_PAGINATION_PER_PAGE = 100

# URL of the login page.
LOGIN_URL = '/login/'

UPLOAD_FILE_DIRS = os.path.join(BASE_DIR, 'upload_files')


#class InvalidString(str):
#    def __mod__(self, other):
#        from django.template.base import TemplateSyntaxError
#        raise TemplateSyntaxError(
#            "Undefined variable or unknown value for: \"%s\"" % other)
#
#TEMPLATE_STRING_IF_INVALID = InvalidString("%s")


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '30/minute'
    },
}

