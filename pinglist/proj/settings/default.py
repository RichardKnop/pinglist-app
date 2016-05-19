# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import etcd
import json
import logging
import sys


logger = logging.getLogger('django')


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
    'apps.alarms',
    'apps.teams',
    'apps.subscriptions',
    'apps.payment_sources',
    'apps.profile',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lib.middleware.LoggedInFlagMiddleware',
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

etcd_client = etcd.Client(
    host=os.getenv('ETCD_HOST', 'localhost'),
    port=int(os.getenv('ETCD_PORT', '2379')),
)

try:
    json_cnf = etcd_client.read('/config/pinglist_app.json').value
    cnf = json.loads(json_cnf)
except etcd.EtcdKeyNotFound as e:
    logger.debug(str(e))
    sys.exit(0)
except ValueError:
    logger.debug(json_cnf)
    sys.exit(0)

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
VERSION = 'v0.0.0'

HOSTNAME = '{}://{}'.format(cnf['Web']['Scheme'], cnf['Web']['Host'])
API_HOST = '{}://{}'.format(cnf['Web']['APIScheme'], cnf['Web']['APIHost'])
OAUTH_CLIENT_ID = cnf['Oauth']['ClientID']
OAUTH_CLIENT_SECRET = cnf['Oauth']['Secret']
OAUTH_DEFAULT_SCOPE = 'read_write'
OAUTH_TOKEN_URL = API_HOST + '/v1/oauth/tokens'
LOGIN_VIEW = 'auth:login'
AFTER_LOGIN_VIEW = 'alarms:index'
AFTER_LOGIN_VIEW_PARAM = 'after_login_view'
FACEBOOK_APP_ID = cnf['Facebook']['AppID']
FACEBOOK_APP_SECRET = cnf['Facebook']['AppSecret']
FACEBOOK_SCOPE = "public_profile,email"
STRIPE_PUBLISHABLE_KEY = cnf['Stripe']['PublishableKey']

CAPTCHA_IMAGE_TEMPLATE = 'home/captcha/image.html'
CAPTCHA_HIDDEN_FIELD_TEMPLATE = 'home/captcha/hidden_field.html'
CAPTCHA_TEXT_FIELD_TEMPLATE = 'home/captcha/text_field.html'
CAPTCHA_FIELD_TEMPLATE = 'home/captcha/field.html'

IOS_LINK = cnf['IOSLink']




