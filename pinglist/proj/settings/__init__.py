# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from .config import load_config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Application definition

INSTALLED_APPS = (
    'django.contrib.postgres',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'captcha',
    'apps.home',
    'apps.auth',
    'apps.web',
    'apps.alarms',
    'apps.teams',
    'apps.subscriptions',
    'apps.payment_sources',
    'apps.settings',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lib.middleware.AccessTokenMiddleware',
)

TIME_ZONE = 'UTC'

ROOT_URLCONF = 'proj.urls'

WSGI_APPLICATION = 'proj.wsgi.application'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'proj', 'static'),
)
STATIC_URL = '/static/'
STATIC_ROOT = '/srv/static'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'proj', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                # 'django.contrib.auth.context_processors.auth',
                # 'django.template.context_processors.debug',
                # 'django.template.context_processors.i18n',
                # 'django.template.context_processors.media',
                'django.template.context_processors.static',
                # 'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}


cnf = load_config()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = cnf['Django']['Secret']

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': cnf['Database']['Engine'],
        'NAME': cnf['Database']['DatabaseName'],
        'USER': cnf['Database']['User'],
        'PASSWORD': cnf['Database']['Password'],
        'HOST': cnf['Database']['Host'],
    },
}

DEBUG = cnf['IsDevelopment']
ALLOWED_HOSTS = '*' if not DEBUG else '.pingli.st'
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

VERSION = 'v0.0.0'
LOGIN_VIEW = 'auth:login'
AFTER_LOGIN_DEFAULT_REDIRECT_URL = '/alarms'
AFTER_LOGIN_REDIRECT_URL_PARAM = 'redirect_to'
AFTER_LOGIN_REDIRECT_QS_PARAM = 'qs_params'
CAPTCHA_IMAGE_TEMPLATE = 'home/captcha/image.html'
CAPTCHA_HIDDEN_FIELD_TEMPLATE = 'home/captcha/hidden_field.html'
CAPTCHA_TEXT_FIELD_TEMPLATE = 'home/captcha/text_field.html'
CAPTCHA_FIELD_TEMPLATE = 'home/captcha/field.html'

HOSTNAME = '{}://{}'.format(cnf['Web']['Scheme'], cnf['Web']['Host'])
API_HOST = '{}://{}'.format(cnf['Web']['APIScheme'], cnf['Web']['APIHost'])
OAUTH_CLIENT_ID = cnf['Oauth']['ClientID']
OAUTH_CLIENT_SECRET = cnf['Oauth']['Secret']
OAUTH_DEFAULT_SCOPE = 'read_write'
OAUTH_TOKEN_URL = API_HOST + '/v1/oauth/tokens'
AWS_REGION = cnf['AWS']['Region']
AWS_ASSETS_BUCKET = cnf['AWS']['AssetsBucket']
FACEBOOK_APP_ID = cnf['Facebook']['AppID']
FACEBOOK_APP_SECRET = cnf['Facebook']['AppSecret']
FACEBOOK_SCOPE = "public_profile,email"
STRIPE_PUBLISHABLE_KEY = cnf['Stripe']['PublishableKey']
IOS_LINK = cnf['Pinglist']['IOSLink']
IS_DEVELOPMENT = cnf['IsDevelopment']

STATICFILES_STORAGE = cnf['Django']['StaticStorage']

# The region to connect to when storing files.
AWS_REGION = cnf['AWS']['Region']

# The S3 bucket used to store static files.
AWS_S3_BUCKET_NAME_STATIC = cnf['AWS']['AssetsBucket']

# The S3 calling format to use to connect to the static bucket.
AWS_S3_CALLING_FORMAT_STATIC = 'boto.s3.connection.OrdinaryCallingFormat'

# The host to connect to for static files (only needed if you are using a non-AWS host)
AWS_S3_HOST_STATIC = ""

# Whether to enable querystring authentication for static files.
AWS_S3_BUCKET_AUTH_STATIC = False

# A prefix to add to the start of all static files.
AWS_S3_KEY_PREFIX_STATIC = 'pinglist-app/'

# The expire time used to access static files.
AWS_S3_MAX_AGE_SECONDS_STATIC = 60*60*24*365  # 1 year.

# A custom URL prefix to use for public-facing URLs for static files.
AWS_S3_PUBLIC_URL_STATIC = 'https://s3-{}.amazonaws.com/{}/{}'.format(
    AWS_REGION,
    AWS_S3_BUCKET_NAME_STATIC,
    AWS_S3_KEY_PREFIX_STATIC,
)

# Whether to set the storage class of static files to REDUCED_REDUNDANCY.
AWS_S3_REDUCED_REDUNDANCY_STATIC = False

# A dictionary of additional metadata to set on the static files.
# If the value is a callable, it will be called with the path of the file on S3.
AWS_S3_METADATA_STATIC = {}
