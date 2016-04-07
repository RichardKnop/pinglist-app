import logging
import requests
from time import time

from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

from . import BaseView, get_facebook_redirect_uri


logger = logging.getLogger(__name__)


class FacebookRedirectView(BaseView):

    def get(self, request, *args, **kwargs):
        # Exchange Facebook authorization code for an access token
        payload = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': get_facebook_redirect_uri(),
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': request.GET.get('code', ''),
        }
        r = requests.get(
            url='https://graph.facebook.com/v2.3/oauth/access_token',
            params=payload,
            allow_redirects=False,
            timeout=1,
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:

            logger.debug(r.text)
            try:
                messages.error(request, r.json()['error']['message'])
            except ValueError:
                messages.error(request, str(e))
            return redirect(settings.LOGIN_VIEW)

        # Login with the access token from Facebook
        try:
            access_token = self.API.facebook_login(r.json()['access_token'])

            # Save the access token in the session
            request.session['access_token'] = access_token
            request.session['access_token_granted_at'] = time()

            # Redirect to the subscriptions page
            return redirect(settings.AFTER_LOGIN_VIEW)

        # Logging in failed, probably incorrect username and/or password
        except self.API.ErrFacebookLoginFailed as e:
            logger.debug(str(e))
            messages.error(request, str(e))
            return redirect(settings.LOGIN_VIEW)

        # Something else went wrong, timeout, network problem etc
        except Exception as e:
            logger.debug(str(e))
            messages.error(request, str(e))
            return redirect(settings.LOGIN_VIEW)
