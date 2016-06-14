from __future__ import absolute_import

from time import time

from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse

from lib.api import API

api_instance = API = API(
    settings.API_HOST,
    settings.OAUTH_CLIENT_ID,
    settings.OAUTH_CLIENT_SECRET,
    settings.OAUTH_DEFAULT_SCOPE,
)


def store_access_token(request, access_token):
    request.session['access_token'] = access_token
    request.session['access_token_granted_at'] = time()


def store_access_token_and_redirect(request, access_token, user):
    store_access_token(request=request, access_token=access_token, user=user)

    try:
        query_string_params = request.session[settings.AFTER_LOGIN_VIEW_QUERYSTRING_PARAM]
    except KeyError:
        query_string_params = {}

    try:
        redirect_url = reverse(request.session[settings.AFTER_LOGIN_VIEW_PARAM])
    except KeyError:
        redirect_url = reverse(settings.AFTER_LOGIN_VIEW)

    if len(query_string_params) > 0:
        redirect_url += '?{}'.format('&'.join(
            ['{}={}'.format(k, vs[0]) for k, vs in query_string_params.iteritems()]
        ))

    return redirect(redirect_url)


def is_logged_in(request):
    # First we try to retrieve the access token from the session
    try:
        access_token = request.session['access_token']
        access_token_granted_at = request.session['access_token_granted_at']

    # Access token not found
    except KeyError:
        return False

    # Second, check that the access token is not expired
    if access_token_granted_at + access_token['expires_in'] < time():
        # Refresh the token
        try:
            store_access_token(
                request=request,
                access_token=api_instance.refresh_token(
                    refresh_token=access_token['refresh_token'],
                ),
            )

        # Refreshing token failed
        except API.APIError:
            return False

        # Something else went wrong, timeout, network problem etc
        except Exception:
            return False

    return True


def logged_in(view):
    def _wrapper(obj, request, *args, **kwargs):
        # User not logged in, redirect to log in view
        if not is_logged_in(request):
            return redirect(settings.LOGIN_VIEW)

        # Everything looks fine, proceed
        return view(obj, request, *args, **kwargs)

    return _wrapper
