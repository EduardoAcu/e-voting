from pathlib import Path
import os
from google.cloud import secretmanager
import json

FERNET_KEY= b'7nFaVXOy7JgEXsB5Qwjycnetu8qsNjNUaIToIPnCkV8='

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-u@d=el-b)c#y)02ne71+k&^8m0xu%y(77(7=#p2+3gn3m##bl^'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '34.0.50.132']

AUTH_USER_MODEL = 'account.Account'



INSTALLED_APPS = [
    'account',
    'main',
    'sweetify',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
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

ROOT_URLCONF = 'core.urls'

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
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'e_voting',
        'USER': 'acuna',
        'PASSWORD': 'admin123',
        'HOST': '127.0.0.1',
        'PORT': '5432',
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


LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(os.getenv('GOOGLE_BUCKET_NAME'))


STATIC_URL = 'https://storage.googleapis.com/{}/'.format(os.getenv('GOOGLE_BUCKET_NAME'))

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

GOOGLE_BUCKET_NAME = 'django-voting'

client = secretmanager.SecretManagerServiceClient()
secret_name = "projects/1087274725247/secrets/django-key/versions/2"
response = client.access_secret_version(name=secret_name)
secret_data = response.payload.data.decode("UTF-8")

OTP = False
OTP_EMAIL = "youremail@gmail.com"
OTP_PASSWORD = "yourpassword"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
