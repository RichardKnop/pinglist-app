from __future__ import absolute_import

from time import time
from urllib import urlencode

from django.shortcuts import redirect
from django.core.urlresolvers import resolve
from django.conf import settings
from django.core.urlresolvers import reverse

from lib.api import API

api_instance = API = API(
    settings.API_HOST,
    settings.OAUTH_CLIENT_ID,
    settings.OAUTH_CLIENT_SECRET,
    settings.OAUTH_DEFAULT_SCOPE,
)


def store_access_token(request, access_token, user):
    request.session['access_token'] = access_token
    request.session['access_token_granted_at'] = time()
    request.session['user'] = user


def store_access_token_and_redirect(request, access_token, user):
    store_access_token(request=request, access_token=access_token, user=user)
    return redirect(get_after_login_redirect_url(request=request))


def is_logged_in(request):
    # First we try to retrieve the access token from the session
    try:
        access_token = request.session['access_token']
        access_token_granted_at = request.session['access_token_granted_at']
        user = request.session['user']

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
                user=user,
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
        if is_logged_in(request):
            # Everything looks fine, proceed
            return view(obj, request, *args, **kwargs)

        # User not logged in, redirect to log in view, remember where to redirect
        redirect_url = request.path
        if len(request.GET) > 0:
            redirect_url += '?{}'.format(urlencode(request.GET))
        return redirect('{}?{}={}'.format(
            reverse(settings.LOGIN_VIEW),
            settings.AFTER_LOGIN_REDIRECT_URL_KEY,
            redirect_url,
        ))

    return _wrapper


def get_after_login_redirect_url(request):
    # Get the redirect URL
    try:
        redirect_to = request.session[settings.AFTER_LOGIN_REDIRECT_URL_KEY]
    except KeyError:
        redirect_to = settings.AFTER_LOGIN_DEFAULT_REDIRECT_URL

    try:
        qs = request.session[settings.AFTER_LOGIN_REDIRECT_SESSION_QS_KEY]
    except KeyError:
        qs = {}

    if len(qs) > 0:
        redirect_to += '?{}'.format(urlencode(qs))

    return redirect_to
