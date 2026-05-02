from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CORE CONFIGURATION
# ==============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-me-in-production-trinetra-security-core')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local Apps
    'access_control',
    'authentication',
    'audit_logs',
    'officer_portal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Trinetra Security Core
    'config.middleware.IPFortressMiddleware',
    'config.middleware.ZeroTrustSessionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'config.context_processors.trinetra_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Session Config (Global)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 300 # 5 Minutes Auto-Logout

# ==============================================================================
# DATABASE & CLOUD CONFIGURATION
# ==============================================================================

# 1. Database
# [PRODUCTION FIX] Proper connection pooling for NeonDB serverless Postgres.
# Previous: conn_max_age=0 caused a fresh TCP+SSL handshake on EVERY request,
# exhausting NeonDB's free-tier connection limit and adding ~300ms latency.
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,     # Reuse connections for 10 min (was 0 = never reuse)
            ssl_require=True
        )
    }
    # [FIX] Add PostgreSQL keepalive parameters to prevent NeonDB's proxy
    # from terminating idle-but-valid connections. This is the #1 cause of
    # "server closed the connection unexpectedly" errors.
    DATABASES['default']['OPTIONS'] = DATABASES['default'].get('OPTIONS', {})
    DATABASES['default']['OPTIONS'].update({
        'keepalives': 1,              # Enable TCP keepalives
        'keepalives_idle': 30,        # Send keepalive after 30s idle (NeonDB timeout is ~60s)
        'keepalives_interval': 10,    # Retry keepalive every 10s
        'keepalives_count': 5,        # Give up after 5 failed keepalives
        'connect_timeout': 30,        # Increased to 30s so NeonDB can wake up
    })
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# [PRODUCTION FIX] Django 4.1+ health check — validates each connection from the
# pool before handing it to a request. Equivalent to SQLAlchemy's pool_pre_ping.
# If a connection was killed by NeonDB's idle timeout, Django silently reconnects
# instead of crashing the request with "connection already closed".
CONN_HEALTH_CHECKS = True

# 2. Static Files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# 3. Security & Azure Networking [CRITICAL FIXES]
# Force trust for Azure's SSL handling
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allowed Hosts — override via ALLOWED_HOSTS env var (comma-separated)
_extra_hosts = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '').split(',') if h.strip()]
ALLOWED_HOSTS = [
    'localhost', '127.0.0.1', '0.0.0.0',
    '.vercel.app',
    '.azurewebsites.net',
    '.railway.app',
] + _extra_hosts

# [CRITICAL] Trust deployment platforms for CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.azurewebsites.net',
    'https://*.railway.app',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Production Toggles
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
TRINETRA_STRICT_FIREWALL = os.environ.get('STRICT_FIREWALL', 'True').lower() == 'true'

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000       # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# Login Config
LOGIN_URL = 'portal_login'
LOGIN_REDIRECT_URL = 'officer_dashboard'
LOGOUT_REDIRECT_URL = 'portal_login'

# ==============================================================================
# LOGGING CONFIGURATION (Production-Grade)
# ==============================================================================
# [PRODUCTION FIX] Structured logging so Azure Log Stream shows categorized,
# searchable entries instead of raw print() output.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} [{name}:{lineno}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # Django internals
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        # Database queries — only show errors in production
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR' if not DEBUG else 'WARNING',
            'propagate': False,
        },
        # Django request handling (4xx/5xx errors)
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        # Trinetra app logs
        'officer_portal': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'trinetra.health': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # Catch-all for any logger we missed
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}