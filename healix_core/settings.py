"""
Django settings for healix_core project.(Production-ready with security and performance optimizations.)
"""
"""
from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
from decouple import config, Csv
import dj_database_url

# ------------------------------------------------------------
# BASE CONFIGURATION
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = config('SECRET_KEY', default='your-secret-key')
DEBUG = config('DEBUG', default=False, cast=bool)

# ------------------------------------------------------------
# HOST CONFIGURATION
# ------------------------------------------------------------
ALLOWED_HOSTS = ['healixind.xyz', 'www.healixind.xyz','10.0.0.2']
RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default=None)
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
ALLOWED_HOSTS.extend(config('ALLOWED_HOSTS', default='', cast=Csv()))

CSRF_TRUSTED_ORIGINS = [
    'https://healixind.xyz',
    'https://www.healixind.xyz',
    'https://healix-backend-goc4.onrender.com',
]
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# ------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # Local apps
    'api',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # optional, for custom templates
        'APP_DIRS': True,  # looks for templates inside each app's "templates" folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by admin
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------------------------
# URLS & WSGI
# ------------------------------------------------------------
ROOT_URLCONF = 'healix_core.urls'
WSGI_APPLICATION = 'healix_core.wsgi.application'

# ------------------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{os.path.join(BASE_DIR, "db.sqlite3")}',
        conn_max_age=600
    )
}

# ------------------------------------------------------------
# AUTHENTICATION & REST FRAMEWORK
# ------------------------------------------------------------
AUTH_USER_MODEL = 'api.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# ------------------------------------------------------------
# STATIC & MEDIA FILES
# ------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------
# CORS SETTINGS
# ------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
 
# ------------------------------------------------------------
# EMAIL CONFIGURATION — USING RES
# ------------------------------------------------------------
RESEND_API_KEY = config('RESEND_API_KEY', default='')

# The sender email must be verified in Resend
DEFAULT_FROM_EMAIL = 'Healix <no-reply@healixind.xyz>'

# ------------------------------------------------------------
# SECURITY SETTINGS (Recommended for Production)
# ------------------------------------------------------------
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ------------------------------------------------------------
# LOGGING (Optional - helps debug Render issues)
# ------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

"""


"""
Django code for Development phase.
"""


# """
from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
from decouple import config, Csv
import dj_database_url
from django_redis import get_redis_connection
# ------------------------------------------------------------
# BASE CONFIGURATION
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1")

SECRET_KEY = os.getenv('SECRET_KEY', default='your-secret-key')
DEBUG = config('DEBUG', default=True, cast=bool)

# ------------------------------------------------------------
# HOST CONFIGURATION
# ------------------------------------------------------------
ALLOWED_HOSTS = ['healixind.xyz', 'www.healixind.xyz','10.0.2.2','localhost','127.0.0.1','0.0.0.0','192.168.29.196']

CSRF_TRUSTED_ORIGINS = [
    'http://10.0.2.2:8000',
    'http://127.0.0.1:8000',
    'http://0.0.0.0:8000',
    'http://192.168.29.196:8000',
    # 'http://192.168.29.196:8000',
]


# ------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'channels',
    # Local apps
    'api',
]
ASGI_APPLICATION = "healix_core.asgi.application"



CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ.get("REDIS_HOST", "127.0.0.1"), 6379)],
            # You can also use a URL if REDIS_URL environment variable is set
            # "hosts": [os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1")],
        },
    },
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # optional, for custom templates
        'APP_DIRS': True,  # looks for templates inside each app's "templates" folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by admin
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------------------------
# URLS & WSGI
# ------------------------------------------------------------
ROOT_URLCONF = 'healix_core.urls'
WSGI_APPLICATION = 'healix_core.wsgi.application'

# ------------------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------------------
# ------------------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,  # Using database 1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# ------------------------------------------------------------
# AUTHENTICATION & REST FRAMEWORK
# ------------------------------------------------------------
AUTH_USER_MODEL = 'api.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# ------------------------------------------------------------
# STATIC & MEDIA FILES
# ------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------
# CORS SETTINGS
# ------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
 
# ------------------------------------------------------------
# EMAIL CONFIGURATION — USING RES
# ------------------------------------------------------------
RESEND_API_KEY = config('RESEND_API_KEY', default='')

# The sender email must be verified in Resend
DEFAULT_FROM_EMAIL = 'Healix <no-reply@healixind.xyz>'

# ------------------------------------------------------------
# SECURITY SETTINGS (Recommended for Production)
# ------------------------------------------------------------
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_PROXY_SSL_HEADER = None


# ------------------------------------------------------------
# LOGGING (Optional - helps debug Render issues)
# ------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
# """