from time import time

from django.shortcuts import redirect
from django.core.urlresolvers import reverse, resolve
from django.core.urlresolvers import NoReverseMatch, Resolver404
from django.conf import settings

from . import API, store_access_token


def logged_in(view):

    def _wrapper(obj, request, *args, **kwargs):
        # First we try to retrieve the access token from the session
        try:
            access_token = request.session['access_token']
            access_token_granted_at = request.session['access_token_granted_at']

        # Access token not found
        except KeyError:
            try:
                resolve_match = resolve(request.get_full_path())
                return redirect('{}?{}={}:{}'.format(
                    reverse(settings.LOGIN_VIEW),
                    settings.AFTER_LOGIN_VIEW_PARAM,
                    resolve_match.namespaces[0],
                    resolve_match.url_name,
                ))
            except (NoReverseMatch, Resolver404):
                return redirect(settings.LOGIN_VIEW)

        # Second, check that the access token is not expired
        if access_token_granted_at + access_token['expires_in'] < time():
            # Refresh the token
            try:
                store_access_token(
                    request=request,
                    access_token=API.refresh_token(
                        refresh_token=access_token['refresh_token'],
                    ),
                )

            # Logging in failed, probably incorrect username and/or password
            except API.ErrRefreshTokenFailed:
                return redirect(settings.LOGIN_VIEW)

            # Something else went wrong, timeout, network problem etc
            except Exception:
                return redirect(settings.LOGIN_VIEW)

        # Set logged in flag to true
        request.logged_in = True

        # Everything looks fine, proceed
        return view(obj, request, *args, **kwargs)
    return _wrapper
