# Django settings for mainweb project.
import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zcmcl$f#xbkwj49!l#%b9q#zib(u#$0%8g^#xeg27uv*im2)zd'

# SECURITY WARNING: don't run with debug turned on in production!
# Set DEBUG to True for local development, and False for production.
# You can use an environment variable to control this.
# It will be True unless DJANGO_DEBUG is set to 'False'
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

# When DEBUG is False, you MUST add your domain names here.
# DO NOT use ['*'] in production, as it is a security vulnerability.
# Add your actual Cloud Run service URLs and any custom domains.
ALLOWED_HOSTS = [
    'website-932534087542.asia-southeast1.run.app',
    'website-xvhbgr5zoq-as.a.run.app',
    # Add your custom domain when you set it up
    'akhilkarwal.com',
    'www.akhilkarwal.com',
    # For local development
    'localhost',
    '127.0.0.1',
]

# Redirect non-WWW to WWW for SEO and consistency.
# This is handled by Django's CommonMiddleware and only works when DEBUG=False.
PREPEND_WWW = not DEBUG


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'persinfo',  # Custom app for personal information management
    'compressor',  # For asset minification
    'django.contrib.sites',  # For site framework
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # IMPORTANT: Add this for serving static files in production
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'mainweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'mainweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
# When not in debug mode, use a CDN if the CDN_HOST environment variable is set.
if not DEBUG:
    CDN_HOST = os.environ.get('CDN_HOST')
    if CDN_HOST:
        STATIC_URL = f'https://{CDN_HOST}/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles' # This is where collectstatic will gather files

# Use django-compressor to minify and Whitenoise to serve compressed/hashed files
STATICFILES_STORAGE = 'compressor.storage.CompressorManifestStaticFilesStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # Add this
    'compressor.finders.CompressorFinder',
)


# Media files (user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles' # This is where user-uploaded files will be stored

# Django Sites Framework
SITE_ID = 1 # This tells Django which Site object to use by default

# CSRF Configuration for Production
# This is crucial when DEBUG is False and you're deploying to a custom domain/Cloud Run URL
CSRF_TRUSTED_ORIGINS = [
    'https://website-932534087542.asia-southeast1.run.app',
    'https://website-xvhbgr5zoq-as.a.run.app',
    'https://akhilkarwal.com',
    'https://www.akhilkarwal.com',
    # For local development
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
# In development (DEBUG=True), these should be False because the dev server
# runs over HTTP. In production (DEBUG=False), they should be True.
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

# HTTPS/Security Settings for Production
# Redirect all HTTP requests to HTTPS.
SECURE_SSL_REDIRECT = not DEBUG

# HSTS (HTTP Strict Transport Security) settings.
# Instructs the browser to only use HTTPS for the next 30 days.
# WARNING: Start with a small value (e.g., 3600 for 1 hour) and increase once you are
# confident that your site is fully functional over HTTPS.
SECURE_HSTS_SECONDS = 2592000 if not DEBUG else 0  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

# Caching Configuration
# https://docs.djangoproject.com/en/5.2/topics/cache/
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR / "django_cache",
    }
}

# Cache middleware settings
CACHE_MIDDLEWARE_ALIAS = "default"  # Which cache to use.
CACHE_MIDDLEWARE_SECONDS = 900  # 15 minutes.
CACHE_MIDDLEWARE_KEY_PREFIX = "portfolio"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WHITENOISE_MAX_AGE = 60 * 60  # 1 hour

# Django Compressor settings
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = not DEBUG  # Creates minified files during `collectstatic`
