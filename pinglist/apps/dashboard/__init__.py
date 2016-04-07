from __future__ import absolute_import

from django.conf import settings

from apps.api import API


API = API(
    settings.API_HOST,
    settings.OAUTH_CLIENT_ID,
    settings.OAUTH_CLIENT_SECRET,
    settings.OAUTH_DEFAULT_SCOPE,
)