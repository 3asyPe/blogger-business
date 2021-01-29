import os

from BloggerBusiness.google_api import google_conf
from celery.schedules import crontab

from . import secret
from . import languages


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
SECRET_KEY = secret.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DOMAIN_NAME = "http://localhost:8000/"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'bloggerandbusiness@gmail.com' 
EMAIL_HOST_PASSWORD = secret.EMAIL_HOST_PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "BLOGGER&BUSINESS <bloggerandbusiness@gmail.com>"
DEFAULT_EMAIL_ACTIVATION_EXPIRE_DAYS = 1

MANAGERS = (
    ("Alex Kvasha", "bloggerandbusiness@gmail.com"),
)

ADMINS = MANAGERS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'phonenumber_field',
    'storages',
    'django_celery_beat',

    # Local
    'account',
    'application',
    'blogger',
    'business',
    'emails',
    'offer',
    'youtube',
]


AUTH_USER_MODEL = "account.User"

BLOG_LANGUAGES = languages.iso_639_choices

# TODO location
COUNTRIES = [
    ("BLR", "Belarus"),
    ("RUS", "Russia"),
    ("USA", "United States of America"),
]

CITIES = [
    ("MINSK", "Minsk"),
    ("MOSKOW", "Moskow"),
    ("WASHINGTON", "Washington"),
]

BLOG_SPECIALIZATIONS = [
    ("TECH", "Tech"),
    ("FUN CONTENT", "Fun content"),
    ("BEAUTY", "Beauty"),
    ("TRAVEL", "Travel"),
    ("KIDS", "Kids"),
    ("SPORT", "Sport"),
    ("HUMOR", "Humor"),
    ("SOCIETY", "Society"),
    ("BUSINESS/FINANCES", "Business/Finances"),
    ("DESIGN", "Design"),
    ("VIDEO GAMES", "Video games"),
    ("ANIMALS", "Animals"),
    ("IT", "IT"),
    ("CREATIVITY", "Creativity"),
    ("FOOD/DRINKS", "Food/Drinks"),
    ("LIFESTYLE", "Lifestyle"),
    ("MUSIC/MOVIES", "Music/Movies"),
    ("EDUCATION", "Education"),
    ("HEALTH", "Health"),
    ("WEB-SITES/APPLICATIONS", "Web-sites/Applications"),
    ("AUTO/MOTO", "Auto/Moto"),
    ("BOOKS", "Books"),
    ("HOUSE/RENOVATION", "House/Renovation"),
]

SEXES = [
    ("M", "MAN"),
    ("W", "WOMAN"),
]

AGE_GROUPS = [
    ("13–17", "13–17 years"),
    ("18–24", "18–24 years"),
    ("25–34", "25–34 years"),
    ("35–44", "35–44 years"),
    ("45–54", "45–54 years"),
    ("55–64", "55–64 years"),
    ("65+", "65+ years"),
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

LOGIN_URL = '/login'
LOGOUT_REDIRECT_URL = '/login'

ROOT_URLCONF = 'BloggerBusiness.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
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

WSGI_APPLICATION = 'BloggerBusiness.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blogger-business',
        'USER': secret.DATABASE_USER,
        'PASSWORD': secret.DATABASE_PASSWORD,
        'HOST': 'localhost',
        'POST': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "static_root")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media_root")

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

CELERY_BROKER_URL = secret.CELERY_BROKER_URL

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    "scheduled_task": {
        "task": "youtube.tasks.update_all_channel_statistics_task",
        "schedule": crontab(minute=0, hour=0),
    }
}

# SSL/TLS
CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "http://"
SECURE_PROXY_SSL_HEADER         = None
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_SECONDS             = None
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_FRAME_DENY               = False
