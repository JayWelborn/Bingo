"""
Django settings for bingo project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
SECRETS = os.path.join(PROJECT_DIR, 'secrets')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if os.getenv('BUILD_ON_TRAVIS', None):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = False
    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'travis_db.sqlite3'),
        }
    }
else:
    with open(os.path.join(SECRETS, 'django-secret.key'), 'r') as f:
        SECRET_KEY = f.readline().strip()

    DEBUG = True

    # Database
    # https://docs.djangoproject.com/en/2.1/ref/settings/#databases
    with open(os.path.join(SECRETS, 'database.password'), 'r') as f:
        DB_PASSWORD = f.readline().strip()

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'bingo',
            'USER': 'bingo',
            'PASSWORD': DB_PASSWORD,
            'HOST': 'localhost',
            'PORT': '',
        }
    }


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# Application definitions
INSTALLED_APPS = [
    'django.contrib.sites',
    'registration',  # Django-registraion-redux
    'django.contrib.auth',
    'home',
    'auth_extension',
    'cards',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',  # Enable social authentication
    'rest_framework',  # Make REST Api
    'rest_framework.authtoken',  # Enable Token Authentication
    'allauth',  # Adds multiple authentication schemes
    'allauth.account',
    'rest_auth',
    'rest_auth.rest_registration',  # Registration through API
    'crispy_forms',  # More clean form handling
    'api',  # REST API
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Social Auth Middleware
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'bingo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # For social auth
                'social_django.context_processors.login_redirect',  # Social
            ],
        },
    },
]

WSGI_APPLICATION = 'bingo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8,}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Authentication back ends
# https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#specifying-authentication-backends
# https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Password Hashers
# https://docs.djangoproject.com/en/1.11/topics/auth/passwords/

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

# Media files (images uploaded via admin page/authenticated users)
# https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-MEDIA_URL
MEDIA_URL = '/media/'

# Add Email info
# https://docs.djangoproject.com/en/1.11/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'jesse.welborn@gmail.com'
EMAIL_HOST_USER = 'jesse.welborn@gmail.com'

with open(os.path.join(SECRETS, 'email.password'), 'r') as f:
            EMAIL_HOST_PASSWORD = f.readline().strip()

# Registration Redux Settings
SITE_ID = 1
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
REGISTRATION_OPEN = True
LOGIN_REDIRECT_URL = '/profile/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
ACCOUNT_EMAIL_VERIFICATION = 'none'


# Test Specific Settings
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }

    CACHE_MIDDLEWARE_SECONDS = 0

# Social Auth Settings
with open(os.path.join(SECRETS, 'github-auth.id'), 'r') as f:
            SOCIAL_AUTH_GITHUB_KEY = f.readline().strip()

with open(os.path.join(SECRETS, 'github-auth.key'), 'r') as f:
            SOCIAL_AUTH_GITHUB_SECRET = f.readline().strip()

with open(os.path.join(SECRETS, 'twitter-auth.key'), 'r') as f:
            SOCIAL_AUTH_TWITTER_KEY = f.readline().strip()

with open(os.path.join(SECRETS, 'twitter-auth.secret'), 'r') as f:
            SOCIAL_AUTH_TWITTER_SECRET = f.readline().strip()

with open(os.path.join(SECRETS, 'facebook-auth.key'), 'r') as f:
            SOCIAL_AUTH_FACEBOOK_KEY = f.readline().strip()

with open(os.path.join(SECRETS, 'facebook-auth.secret'), 'r') as f:
            SOCIAL_AUTH_FACEBOOK_SECRET = f.readline().strip()

SOCIAL_AUTH_LOGIN_ERROR_URL = '/profile/settings/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/profile/settings/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# Rest API Settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

# Rest Auth Settings
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'api.serializers.UserSerializer'
}
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False

# Allow API requests from the following URLs
CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    '127.0.0.1:3000',
    'bingo-frontend.herokuapp.com/',
)
