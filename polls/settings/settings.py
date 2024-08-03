import os

from pathlib import Path
from .settings_secret import SECRET_KEY, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

# * add your SECRET_KEY, ALLOWED_HOSTS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

# EXAMPLE:
# SECRET_KEY = 'django-insecure-r-,`4tcx/nfp)_:;{g[*^kb3js>ahwf9r6q!4#%u!k!n#p0z!b'
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# EMAIL_HOST_USER = 'email@email.com'
# EMAIL_HOST_PASSWORD = 'bcvx grhb sdgf sfgd'  # for gmail

BASE_DIR = Path(__file__).resolve().parent.parent

LOGIN_URL = '/registration/signin/'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/runtime.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


# Application definition
INSTALLED_APPS = [
    # my apps
    'polls',
    'core.apps.CoreConfig',
    'registration.apps.RegistrationConfig',

    # default apps 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party apps
    'django_gulp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'polls.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'polls.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'registration.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
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

STATIC_URL = '/prefix/'
STATIC_ROOT = 'www/public'
STATICFILES_DIRS = [
    # 'www/public/static',
]
MEDIA_ROOT = 'media'
MEDIA_URL = 'media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

CORS_ORIGIN_ALLOW_ALL = True

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_AGE = 86400
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

X_FRAME_OPTIONS = 'DENY'
