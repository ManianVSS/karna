import os
from pathlib import Path

import django_env_overrides

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j)9ww_2o%n0(-)2j1s8ew$lwbxqz&*dl3q8e&_&t^&fpm17-=c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # bool(os.getenv("DEBUG", 'True'))

ALLOWED_HOSTS = ["*"]
X_FRAME_OPTIONS = 'SAMEORIGIN'
# APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',  # Added for Django Rest Framework
    'rest_framework.authtoken',
    'rest_framework_swagger',

    'django_filters',  # Added for filtering

    'corsheaders',

    'import_export',  # Import export

    # 'advanced_filters',  # Advanced filters

    # 'guardian',

    'massadmin',

    # 'revproxy', # Reverse proxy config

    'dbbackup',  # django-dbbackup

    'api',  # Project modules
]

MIDDLEWARE = [
    'api.middlewares.CustomCorsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'build'), os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'api.contextprocessors.site_configuration',
            ],
            # For swagger
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


if os.getenv("mode", "staging") == "production":
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DATABASE__ENGINE', 'django.db.backends.postgresql_psycopg2'),
            'NAME': os.getenv('DATABASE__NAME', 'karna'),
            'USER': os.getenv('DATABASE__USER', 'karnaadmin'),
            'PASSWORD': os.getenv('DATABASE__PASSWORD', 'karnaadmin@123'),
            'HOST': os.getenv('DATABASE__HOST', 'localhost'),
            'PORT': os.getenv('DATABASE__PORT', '5432'),
        }
    }
else:
    os.makedirs(os.getenv('DATA_MOUNT_DIR', str(BASE_DIR)) + '/data', exist_ok=True, )
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.getenv('DATA_MOUNT_DIR', str(BASE_DIR)) + '/data/db.sqlite3',
        }
    }
print("Database object is :", str(DATABASES))

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'  # 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/data/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), os.path.join(BASE_DIR, 'build'),
                    os.path.join(BASE_DIR, 'build/static'),
                    os.path.join(BASE_DIR, STATIC_URL)]

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_BASE_NAME = 'data'
MEDIA_ROOT = os.path.join(os.getenv('DATA_MOUNT_DIR', BASE_DIR), MEDIA_BASE_NAME)
# os.makedirs(MEDIA_ROOT, exist_ok=True)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend', # this is default
#     'guardian.backends.ObjectPermissionBackend',
# )

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],

    # Added for swagger
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    # Pagination
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPaginationExtn',
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.PageNumberPaginationExtn',

    # Added for filtering
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ]

}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "access-control-allow-origin",
    "access-control-allow-methods",
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
# CORS_ALLOWED_ORIGIN_REGEXES = ['http://localhost:3000', 'http://127.0.0.1:3000']


# ATTACHMENT_DIR = "./attachments"
# os.makedirs(ATTACHMENT_DIR, exist_ok=True)
django_env_overrides.apply_to(globals())
