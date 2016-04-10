import sys

from proj.settings.default import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tbd(pv7679n_w-t++*s_*oon&#v0ubhkxhzvlq51ko2+=dt*z#'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pinglist_app',
        'USER': 'pinglist_app',
        'PASSWORD': '',
        'HOST': '',
    },
}

DEBUG = True

HOSTNAME = 'https://pingli.st'
API_HOST = 'https://api.pingli.st'
OAUTH_CLIENT_ID = 'test_client_1'
OAUTH_CLIENT_SECRET = 'test_secret'
OAUTH_DEFAULT_SCOPE = 'read_write'
OAUTH_TOKEN_URL = API_HOST + '/v1/oauth/tokens'
LOGIN_VIEW = 'auth:login'
AFTER_LOGIN_VIEW = 'subscriptions:index'
AFTER_LOGIN_VIEW_PARAM = 'after_login_view'
FACEBOOK_APP_ID = 'facebook_app_id'
FACEBOOK_APP_SECRET = 'facebook_app_secret'
FACEBOOK_SCOPE = "public_profile,email"
STRIPE_PUBLISHABLE_KEY = "stripe_publishable_key"
STRIPE_SECRET_KEY = "stripe_secret_key"