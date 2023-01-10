import os
from pathlib import Path
import environ

env = environ.Env()
environ.Env.read_env(env_file='../.env')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.get_value('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # additional libraries
    "corsheaders",
    'rest_framework.authtoken',
    'rest_framework',
    'djoser',

    # apps
    'authorization.apps.AuthorizationConfig',
    'booking.apps.BookingConfig',
    'api.apps.ApiConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rental.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'rental/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rental.wsgi.application'

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": env.get_value('DB_PASSWORD'),
        "HOST": "localhost",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'rental/static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGOUT_REDIRECT_URL = 'login'

# Logger settings

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'WARNING',
#             'class': 'logging.FileHandler',
#             'filename': 'log.log',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'booking_logger': {
#             'handler': ['file'],
#             'level': 'WARNING',
#         }
#     }
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs.log',
            'formatter': 'default',
        },
    },
    'loggers': {
        'booking': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# rest framework setup

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}
