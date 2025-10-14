# from pathlib import Path
# import os
# from dotenv import load_dotenv
# from decouple import config, Csv
# import dj_database_url
# from datetime import timedelta

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Load Environment Variables from the .env file in your project root
# load_dotenv(os.path.join(BASE_DIR, '.env'))

# SECRET_KEY = config('SECRET_KEY')

# # DEBUG is set to False in production by default
# DEBUG = config('DEBUG', default=False, cast=bool)

# # --- FINAL, ROBUST ALLOWED_HOSTS CONFIGURATION ---
# ALLOWED_HOSTS = []
# RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default=None)
# if RENDER_EXTERNAL_HOSTNAME:
#     ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# # Also add hosts from the .env file, including your custom domain
# ALLOWED_HOSTS.extend(config('ALLOWED_HOSTS', default='', cast=Csv()))

# # --- CSRF Configuration for Production (THE FIX) ---
# if RENDER_EXTERNAL_HOSTNAME:
#     CSRF_TRUSTED_ORIGINS = ['https://' + RENDER_EXTERNAL_HOSTNAME]


# # --- Application definition ---
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'whitenoise.runserver_nostatic', # For serving static files in development
#     'django.contrib.staticfiles',
#     # Third-party apps
#     'rest_framework',
#     'rest_framework_simplejwt',
#     'corsheaders',
#     # Your apps
#     'api',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware', # WhiteNoise middleware is crucial
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'healix_core.urls'
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
# WSGI_APPLICATION = 'healix_core.wsgi.application'


# # --- Database Configuration ---
# DATABASES = {
#     'default': dj_database_url.config(
#         default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
#         conn_max_age=600
#     )
# }

# # --- Password validation, Internationalization, etc. ---
# AUTH_PASSWORD_VALIDATORS = []
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # --- Static files (CSS, JavaScript, Images) ---
# STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# CORS_ALLOW_ALL_ORIGINS = True
# AUTH_USER_MODEL = 'api.User'

# # --- REST FRAMEWORK & JWT SETTINGS ---
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     )
# }
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
# }

# # --- EMAIL SETTINGS (using environment variables) ---
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# # ```

# # ### What to Do Next

# # 1.  **Commit and Push**: Save the updated `settings.py` file, then commit and push this change to your GitHub repository.
# #     ```bash
# #     git add healix_core/settings.py
# #     git commit -m "Fix: Add CSRF_TRUSTED_ORIGINS for production"
# #     git push
    
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
#         # Use 'INFO' to capture more details, or 'WARNING' for less noise in production.
#         'level': 'INFO',
#     },
# }

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
ALLOWED_HOSTS = ['healixind.xyz', 'www.healixind.xyz']
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
# EMAIL CONFIGURATION — USING RESEND
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
