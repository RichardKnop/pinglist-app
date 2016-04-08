import logging
import requests

from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

from apps.api import store_access_token_and_redirect

from . import BaseView, get_facebook_redirect_uri


logger = logging.getLogger(__name__)


class FacebookRedirectView(BaseView):

    def get(self, request, *args, **kwargs):
        # Facebook redirected with an error
        if 'error' in request.GET:
            messages.error(request, request.GET.get('error_description'))
            return redirect(settings.LOGIN_VIEW)

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
            return store_access_token_and_redirect(
                request=request,
                access_token=self.API.facebook_login(r.json()['access_token']),
            )

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
