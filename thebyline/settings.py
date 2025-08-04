import os
from pathlib import Path
from decouple import config, Csv
# import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'storages'
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
]

ROOT_URLCONF = 'thebyline.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'thebyline.wsgi.application'

# DATABASE: PostgreSQL via DATABASE_URL
# DATABASES = {
#     'default': dj_database_url.config(default = str(config('DB_URL')))
# }


# Default DB
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
}

# PASSWORD VALIDATION
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

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# STATIC & MEDIA FILES
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Additional locations of static files
STATICFILES_DIRS = [
    BASE_DIR / 'blog' / 'static',
]

# Cloudflare R2 Configuration
AWS_ACCESS_KEY_ID = config("CLOUDFLARE_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("CLOUDFLARE_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("CLOUDFLARE_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = config("CLOUDFLARE_R2_ENDPOINT")

# Cloudflare R2 specific settings
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_ADDRESSING_STYLE = "virtual"
AWS_S3_REGION_NAME = 'auto'  # Cloudflare R2 uses 'auto' region
AWS_S3_USE_SSL = True
AWS_S3_VERIFY = True

# Storage location for organizing files
AWS_LOCATION = 'media'

# Custom domain for public access (your R2 custom domain)
AWS_S3_CUSTOM_DOMAIN = config("CLOUDFLARE_R2_CUSTOM_DOMAIN", default=None)

# Django 4.2+ storage configuration
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "endpoint_url": AWS_S3_ENDPOINT_URL,
            "region_name": AWS_S3_REGION_NAME,
            "signature_version": AWS_S3_SIGNATURE_VERSION,
            "file_overwrite": AWS_S3_FILE_OVERWRITE,
            "default_acl": AWS_DEFAULT_ACL,
            "querystring_auth": AWS_QUERYSTRING_AUTH,
            "addressing_style": AWS_S3_ADDRESSING_STYLE,
            "use_ssl": AWS_S3_USE_SSL,
            "verify": AWS_S3_VERIFY,
            "location": AWS_LOCATION,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media files configuration
if AWS_S3_CUSTOM_DOMAIN:
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
else:
    MEDIA_URL = 'https://pub-5d5efcd0a9c84f73933ac01758beb8d5.r2.dev'

MEDIA_ROOT = BASE_DIR / 'media'

# DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# THIRD PARTY API
RAPIDAPI_KEY = config('RAPIDAPI_CRICKBUZZ_KEY')


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#         'boto3': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#         'botocore': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#         'django.request': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }
