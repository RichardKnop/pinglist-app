from __future__ import absolute_import

from django.conf import settings
from django.core.urlresolvers import reverse


def get_facebook_redirect_uri():
    redirect_uri = reverse('auth:facebook_redirect')
    return '{}{}'.format(settings.HOSTNAME, redirect_uri)


def get_facebook_authorize_uri(state):
    return 'https://www.facebook.com/dialog/oauth?client_id={}&scope={}&state={}&redirect_uri={}'.format(
        settings.FACEBOOK_APP_ID,
        settings.FACEBOOK_SCOPE,
        state,
        get_facebook_redirect_uri(),
    )
