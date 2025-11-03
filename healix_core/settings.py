# from pathlib import Path
# import os
# import dj_database_url
# from decouple import config # Make sure 'python-decouple' is in your requirements.txt
# from datetime import timedelta

# # from pathlib import Path
# # import os
# # from datetime import timedelta
# # from dotenv import load_dotenv
# from decouple import config, Csv
# # import dj_database_url
# from django_redis import get_redis_connection
# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Load .env file if it exists (for local development)
# if os.path.exists(BASE_DIR / '.env'):
#     from dotenv import load_dotenv
#     load_dotenv(os.path.join(BASE_DIR, '.env'))

# # --- SECURITY SETTINGS ---
# # Reads from Render's env vars, or your local .env, or a default
# SECRET_KEY = config('SECRET_KEY', default='django-insecure-local-key-for-dev')
# DEBUG = config('DEBUG', default=True, cast=bool)

# # Get ALLOWED_HOSTS from env var.
# # On Render, set this to 'healix-backend-1.onrender.com'
# # The .split(',') allows you to provide a comma-separated list
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')


# # --- APPLICATION DEFINITION ---
# INSTALLED_APPS = [
#     'daphne', # Must be first
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'whitenoise.runserver_nostatic', # Use this for static files in dev
#     'django.contrib.staticfiles',

#     # Third-party apps
#     'rest_framework',
#     'rest_framework_simplejwt',
#     'corsheaders',
#     'channels',
#     'django_redis', # Added for Redis cache/channels
    
#     # Local apps
#     'api',
# ]

# # --- MIDDLEWARE ---
# # 'whitenoise.middleware.WhiteNoiseMiddleware' goes HERE
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware', # <-- CORRECT LOCATION
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'healix_core.urls'
# WSGI_APPLICATION = 'healix_core.wsgi.application'
# ASGI_APPLICATION = "healix_core.asgi.application"

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [], 
#         'APP_DIRS': True, 
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]


# # --- DATABASE CONFIGURATION ---
# # This reads the DATABASE_URL from Render's environment
# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL'), # Reads from .env
#         conn_max_age=600
#     )
# }

# # --- REDIS & CHANNELS ---
# # This reads the REDIS_URL from Render's environment
# REDIS_URL = config('REDIS_URL', default='redis://127.0.0.1:6379/1')

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [REDIS_URL],
#         },
#     },
# }

# # This sets up Redis as your main cache
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": REDIS_URL,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }


# # --- AUTHENTICATION & REST FRAMEWORK ---
# AUTH_USER_MODEL = 'api.User'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated', # Default to secure
#     ),
# }

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
#     # You might need this for secure cookies in production
#     # "AUTH_COOKIE_SECURE": config('DEBUG', default=True, cast=bool) == False, 
# }

# # --- STATIC & MEDIA FILES ---
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # For Render
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # --- CORS SETTINGS ---
# CORS_ALLOW_ALL_ORIGINS = True # Good for development
# CORS_ALLOW_CREDENTIALS = True
# # In production, you'd want this:
# # CORS_ALLOWED_ORIGINS = [
# #     "https://your-flutter-app-domain.com",
# # ]

# # --- EMAIL ---
# RESEND_API_KEY = config('RESEND_API_KEY', default='')
# DEFAULT_FROM_EMAIL = 'Healix <no-reply@healixind.xyz>'


# """
# from pathlib import Path
# import os
# from datetime import timedelta
# from dotenv import load_dotenv
# from decouple import config, Csv
# import dj_database_url
# from django_redis import get_redis_connection
# # ------------------------------------------------------------
# # BASE CONFIGURATION
# # ------------------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv(os.path.join(BASE_DIR, '.env'))
# REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1")

# SECRET_KEY = os.getenv('SECRET_KEY', default='your-secret-key')
# DEBUG = config('DEBUG', default=True, cast=bool)

# # ------------------------------------------------------------
# # HOST CONFIGURATION
# # ------------------------------------------------------------
# ALLOWED_HOSTS = ['healixind.xyz', 'www.healixind.xyz','10.0.2.2','localhost','127.0.0.1','0.0.0.0','10.221.253.226']

# CSRF_TRUSTED_ORIGINS = [
#     'http://10.0.2.2:8000',
#     'http://127.0.0.1:8000',
#     'http://0.0.0.0:8000',
#     'http://10.221.253.226:8000',
#     # 'http://192.168.29.196:8000',
# ]


# # ------------------------------------------------------------
# # APPLICATIONS
# # ------------------------------------------------------------
# INSTALLED_APPS = [
#     'daphne',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'whitenoise.runserver_nostatic',
#     'django.contrib.staticfiles',

#     # Third-party apps
#     'rest_framework',
#     'rest_framework_simplejwt',
#     'corsheaders',
#     'channels',
#     # Local apps
#     'api',
# ]
# ASGI_APPLICATION = "healix_core.asgi.application"



# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [(os.environ.get("REDIS_HOST", "127.0.0.1"), 6379)],
#             # You can also use a URL if REDIS_URL environment variable is set
#             # "hosts": [os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1")],
#         },
#     },
# }


# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, 'templates')],  # optional, for custom templates
#         'APP_DIRS': True,  # looks for templates inside each app's "templates" folder
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',  # required by admin
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# # ------------------------------------------------------------
# # MIDDLEWARE
# # ------------------------------------------------------------
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# # ------------------------------------------------------------
# # URLS & WSGI
# # ------------------------------------------------------------
# ROOT_URLCONF = 'healix_core.urls'
# WSGI_APPLICATION = 'healix_core.wsgi.application'

# # ------------------------------------------------------------
# # DATABASE CONFIGURATION
# # ------------------------------------------------------------
# # ------------------------------------------------------------
# # DATABASE CONFIGURATION
# # ------------------------------------------------------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }


# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": REDIS_URL,  # Using database 1
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# # ------------------------------------------------------------
# # AUTHENTICATION & REST FRAMEWORK
# # ------------------------------------------------------------
# AUTH_USER_MODEL = 'api.User'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.AllowAny',
#     ),
# }

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
# }

# # ------------------------------------------------------------
# # STATIC & MEDIA FILES
# # ------------------------------------------------------------
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # ------------------------------------------------------------
# # CORS SETTINGS
# # ------------------------------------------------------------
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True
 
# # ------------------------------------------------------------
# # EMAIL CONFIGURATION — USING RES
# # ------------------------------------------------------------
# RESEND_API_KEY = config('RESEND_API_KEY', default='')

# # The sender email must be verified in Resend
# DEFAULT_FROM_EMAIL = 'Healix <no-reply@healixind.xyz>'

# # ------------------------------------------------------------
# # SECURITY SETTINGS (Recommended for Production)
# # ------------------------------------------------------------
# SECURE_HSTS_SECONDS = 0
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# SECURE_BROWSER_XSS_FILTER = False
# SECURE_CONTENT_TYPE_NOSNIFF = False
# SECURE_PROXY_SSL_HEADER = None


# # ------------------------------------------------------------
# # LOGGING (Optional - helps debug Render issues)
# # ------------------------------------------------------------
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'INFO',
#     },
# }
# # """









from pathlib import Path
import os
import dj_database_url
from decouple import config, Csv # Make sure 'python-decouple' is in requirements.txt
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file if it exists (for local development)
if os.path.exists(BASE_DIR / '.env'):
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, '.env'))

# --- SECURITY SETTINGS ---
SECRET_KEY = config('SECRET_KEY', default='django-insecure-local-key-for-dev')
DEBUG = config('DEBUG', default=False, cast=bool) # Set default to False for production

# --- FIX 1: Add your Render URL to ALLOWED_HOSTS ---
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')
# Make sure your Render Env Var for ALLOWED_HOSTS is:
# healix-backend-1.onrender.com


# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'daphne', # Must be first
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # For serving static files in dev
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'channels',
    'django_redis', 
    
    # Local apps
    'api',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <-- This is for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'healix_core.urls'
WSGI_APPLICATION = 'healix_core.wsgi.application'
ASGI_APPLICATION = "healix_core.asgi.application"

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


# --- DATABASE CONFIGURATION ---
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'), # Reads from .env or Render
        conn_max_age=600
    )
}

# --- REDIS & CHANNELS ---
REDIS_URL = config('REDIS_URL', default='redis://127.0.0.1:6379/1')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# --- AUTHENTICATION & REST FRAMEWORK ---
AUTH_USER_MODEL = 'api.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # Default to secure
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# --- STATIC & MEDIA FILES ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CORS SETTINGS ---
CORS_ALLOW_ALL_ORIGINS = True # This is fine for now
CORS_ALLOW_CREDENTIALS = True

# --- FIX 2: Add your Render URL to trusted origins for CSRF ---
CSRF_TRUSTED_ORIGINS = [
    'https://healix-backend-1.onrender.com'
]
# If you have a custom domain, add it here too:
# 'https://www.healixind.xyz'

# --- EMAIL ---
RESEND_API_KEY = config('RESEND_API_KEY', default='')
DEFAULT_FROM_EMAIL = 'Healix <no-reply@healixind.xyz>'

