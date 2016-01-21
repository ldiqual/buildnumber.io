import os
from os.path import join, dirname
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_path = join(dirname(__file__), '../', '.env')
load_dotenv(dotenv_path)

MAILGUN_SECRET_API_KEY = os.environ.get("MAILGUN_SECRET_API_KEY")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")

SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False)

ALLOWED_HOSTS = [
    'buildnumber-io.herokuapp.com',
    'buildnumber.io',
    'api.buildnumber.io'
]

CORS_ORIGIN_WHITELIST = [
    'www.buildnumber.io',
    'buildnumber.io'
]

if DEBUG:
    CORS_ORIGIN_WHITELIST += [
        '127.0.0.1:8080',
        '127.0.0.1:8000',
    ]

print CORS_ORIGIN_WHITELIST

# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'rest_framework',
    'api'
]

MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'buildnumber.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [],
        },
    },
]

WSGI_APPLICATION = 'buildnumber.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if os.environ.get('HEROKU', False):
    DATABASES['default'] = dj_database_url.config()
    DATABASES['default']['CONN_MAX_AGE'] = 500


REST_FRAMEWORK = {
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.auth.TokenAuthentication'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    )
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
