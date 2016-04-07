from time import time

from django.shortcuts import redirect
from django.conf import settings

from . import API


def logged_in(view):

    def _wrapper(obj, request, *args, **kwargs):
        # First we try to retrieve the access token from the session
        try:
            access_token = request.session.get('access_token')
            access_token_granted_at = request.session.get('access_token_granted_at')

        except AttributeError:
            return redirect(settings.LOGIN_VIEW)

        if not access_token or not access_token_granted_at:
            return redirect(settings.LOGIN_VIEW)

        # Second, check that the access token is not expired
        if access_token_granted_at + access_token['expires_in'] < time():
            try:
                # Try to refresh the token
                new_access_token = API.refresh_token(access_token)

                # Save the new access token in the session
                request.session['access_token'] = new_access_token
                request.session['access_token_granted_at'] = time()

            # Logging in failed, probably incorrect username and/or password
            except API.ErrRefrestTokenFailed as e:
                return redirect(settings.LOGIN_VIEW)

            # Something else went wrong, timeout, network problem etc
            except Exception as e:
                return redirect(settings.LOGIN_VIEW)

        # Set logged in flag to true
        request.logged_in = True

        # Everything looks fine, proceed
        return view(obj, request, *args, **kwargs)
    return _wrapper
