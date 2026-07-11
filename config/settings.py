from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ['SECRET_KEY']  # sin default: si falta, la app no arranca
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

CSRF_TRUSTED_ORIGINS = [
    f'https://{h}' for h in ALLOWED_HOSTS
    if h not in ('localhost', '127.0.0.1', '', '*')
]

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # third-party
    'post_office',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # apps core
    'accounts',
    'tokens',
    'psychometrics',
    'mirror',
    'birth',
    'community',
    'practitioners',
    'oraculo',
    'terapeuta',
    'payments',
    'reports',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_LOGIN_BY_CODE_ENABLED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APPS': [{
            'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
            'key': '',
        }],
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_ADAPTER = 'accounts.adapters.SocialAccountAdapter'

ROOT_URLCONF = 'config.urls'

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
                'accounts.context_processors.user_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

_db_url = os.getenv('DATABASE_URL')
if _db_url:
    DATABASES = {'default': dj_database_url.parse(_db_url)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/adios/'

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'endonautas-cache',
    }
}

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
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# AI — proveedor centralizado
# AI_PROVIDER: 'deepseek' | 'openrouter' | 'auto' (default: openrouter si hay key, si no deepseek)
AI_PROVIDER        = os.getenv('AI_PROVIDER', 'auto')
DEEPSEEK_API_KEY   = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_MODEL     = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
# Modelo free por defecto; cambiar a cualquier modelo de openrouter.ai/models
OPENROUTER_MODEL   = os.getenv('OPENROUTER_MODEL', 'google/gemma-4-31b-it:free')
# Modelo para razonamiento clínico del módulo terapeuta (diferenciación y propuesta).
# DeepSeek es confiable en JSON y español; el scoring determinista es la base, la IA solo refina.
AI_MODEL_CLINICO   = os.getenv('AI_MODEL_CLINICO', 'deepseek-chat')

# Email
EMAIL_BACKEND = 'post_office.EmailBackend'
POST_OFFICE = {
    'DEFAULT_PRIORITY': 'now',
    'EMAIL_BACKEND': os.getenv(
        'EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'
    ),
}
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'hola@endonautas.cl')

# Fractones
FRACTON_REWARDS = {
    'test_completed': 8,
    'dimension_completed': 25,
    'streak_weekly': 15,
    'onboarding': 60,
    'first_test': 20,
    'first_espejo': 40,
    'first_dimension': 50,
}
TOKEN_COSTS = {
    'espejo_exchange': 6,
    'ai_insight': 15,
    'oraculo_tarot': 8,
    'oraculo_iching': 6,
    'oraculo_fractal': 5,
    'birth_report': 20,
    'terapeuta_session': 10,
    'report': 40,
}
PLAN_MONTHLY_TOKENS = {
    'free': 80,
    'navegante': 800,
    'practicante': 5000,
    'empresa': 20000,
}
# Pagos — PayPal
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID', '')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET', '')
PAYPAL_MODE = os.getenv('PAYPAL_MODE', 'sandbox')
PAYPAL_WEBHOOK_ID = os.getenv('PAYPAL_WEBHOOK_ID', '')

# Pagos — MercadoPago
MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN', '')
MERCADOPAGO_WEBHOOK_SECRET = os.getenv('MERCADOPAGO_WEBHOOK_SECRET', '')

# Reports — KPI automático semanal
KPI_API_TOKEN = os.getenv('KPI_API_TOKEN', '')
UMAMI_API_KEY = os.getenv('UMAMI_API_KEY', '')
UMAMI_WEBSITE_ID = os.getenv('UMAMI_WEBSITE_ID', 'e03fa69e-9931-411c-9838-7f6ffea90426')
LISTMONK_TX_KPI_TEMPLATE_ID = os.getenv('LISTMONK_TX_KPI_TEMPLATE_ID', '0')
FRANCO_EMAIL = os.getenv('FRANCO_EMAIL', 'fjeriacastro@gmail.com')

REFERRAL_REWARDS = {
    'signup_referrer': 60,
    'signup_referred': 40,
    'conversion_referrer': 250,
}
