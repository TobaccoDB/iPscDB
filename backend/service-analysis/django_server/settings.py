import os
import datetime
import logging

# ===========================
# = Directory Declaractions =
# ===========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_FILE = os.path.join(CURRENT_DIR, 'logs/django_server.log')
STATS_FILE = os.path.join(CURRENT_DIR, 'logs/django_server.log')
ANALYSE_BASE_DIR = "/home/Data_analyse/"

# ===================
# = Global Settings =
# ===================
DEBUG = True
ALLOWED_HOSTS = ["*"]
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False
ROOT_URLCONF = 'django_server.urls'
WSGI_APPLICATION = 'django_server.wsgi.application'
APPEND_SLASH = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# AUTH_USER_MODEL = 'user.User'
# Application definition

# =================
# = CORS Settings =
# =================
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = ["*"]
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
)

# ================
# = JWT Settings =
# ================
JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'Token',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=365 * 2)
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'corsheaders',
    'django_celery_beat',
    'django_celery_results',
    'django_server',
    #'django_server.apps.account',
    #'django_server.apps.user',
    'django_server.apps.analysis'
]

# ==================
# = Rest framework =
# ==================
REST_FRAMEWORK = {
    'PAGINATE_BY': 5,
    'PAGE_SIZE': 15,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 50,
    'DEFAULT_PAGINATION_CLASS': 'django_server.paginations.PageNumberOffsetPagination',
    'NON_FIELD_ERRORS_KEY': '__all__',
    'DEFAULT_RENDERER_CLASSES': (
        'django_server.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'django_server.authentication.JSONWebTokenAuthentication',
    ),
    'EXCEPTION_HANDLER': 'django_server.exception.exception_handler',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_server.middleware.GenericQueryParserMiddleware',
]

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

# ===================
# = Logging Settings=
# ===================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)-12s] %(message)s',
            'datefmt': '%b %d %H:%M:%S'
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 16777216,  # 16megabytes
            'formatter': 'verbose'
        },
        'log_stats': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': STATS_FILE,
            'maxBytes': 16777216,  # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
        # 'sentry': {
        #     'level': 'ERROR',
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler'
        # },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'marketbox': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'stats': {
            'handlers': ['console', 'log_stats'],
            'level': 'INFO',
            'propagate': False,
        },
        'commands': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
}

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# ==================
# = Configurations =
# ==================

from local_settings import *

