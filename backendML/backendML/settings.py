from pathlib import Path
from dotenv import load_dotenv # type: ignore
import os
import pickle
import environ
import dj_database_url
from datetime import timedelta


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# MODELS = os.path.join(BASE_DIR, '/home/clencyc/Dev/Fraud-Detection-Machine-Learning/Models')
model_path = os.path.join("/home/clencyc/Dev/Fraud-Detection-Machine-Learning/Models/best_model_random_forest.pkl")
# Secret Key & Debug
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')

AUTH_USER_MODEL = 'users.User'

# settings.py

# Application Definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',  # Access abstract models
    'django_filters',  # Used with DRF
    'rest_framework',  # DRF package
    'rest_framework.authtoken',
    'corsheaders',  # Required for CORS support
    'core',
    'notifications',
    'reports',
    'users',
    'PaymentProcessing',
    'push_notifications',
    'channels',  # Required for Django Channels (real-time support)
    'testmodel',
    'django_celery_beat',
    'django_apscheduler'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True 
CORS_ALLOWED_ALL_ORIGINS = [
    'http://localhost:3000',
    'https://web-interface-fraud.vercel.app/dashboard'
]
ROOT_URLCONF = 'backendML.urls'

# Templates
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
                'django.template.context_processors.request',  # for auth
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ASGI and Channels Configuration
ASGI_APPLICATION = 'backendML.asgi.application'  # Ensure ASGI application
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"  # Development setup
    }
}

# Database Configuration
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
DATABASES = {
    'default': env.db(),
}

DATABASES = {
    'default': env.db(),
}
# Static Files
STATIC_URL = '/static/'

# Rest Framework Configuration
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    # Use simple JWT for authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_json_api.filters.QueryParameterValidationFilter',
        'rest_framework_json_api.filters.OrderingFilter',
        'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'SEARCH_PARAM': 'filter[search]',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json',
}

# Push Notifications (Optional - configure for your environment)
PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": os.getenv("FCM_API_KEY"),  # Firebase Cloud Messaging Key
    "GCM_API_KEY": os.getenv("GCM_API_KEY"),  # Google Cloud Messaging Key (if needed)
    "APNS_CERTIFICATE": os.getenv("APNS_CERTIFICATE_PATH"),  # Apple push certificate path
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}

# Simple JWT Configuration
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

AUTHENTICATION_BACKENDS = [
    'backendML.backends.EmailBackend',  # Replace 'your_app_name' with the actual app name
    'django.contrib.auth.backends.ModelBackend',
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST ='smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'christineoyiera51@gmail.com'
EMAIL_HOST_PASSWORD = 'nszi znto dpoh nfpg'
