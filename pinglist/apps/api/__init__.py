from __future__ import absolute_import

import requests
from time import time

from django.conf import settings
from django.shortcuts import redirect


class API(object):

    class ErrLoginFailed(Exception):
        pass

    class ErrRefreshTokenFailed(Exception):
        pass

    class ErrFacebookLoginFailed(Exception):
        pass

    def __init__(self, hostname, client_id, client_secret, scope):
        self.hostname = hostname
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope

    # Logs in a user via resource owner credentials grant
    def login(self, username, password):
        r = requests.post(
            self.hostname + '/v1/oauth/tokens',
            auth=(self.client_id, self.client_secret),
            data={
                'grant_type': 'password',
                'username': username,
                'password': password,
                'scope': self.scope,
            },
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.ErrLoginFailed(r.json()['error'])
            except ValueError:
                raise self.ErrLoginFailed(str(e))
        return r.json()

    # Refreshes an access token
    def refresh_token(self, refresh_token):
        r = requests.post(
            self.hostname + '/v1/oauth/tokens',
            auth=(self.client_id, self.client_secret),
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            },
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.ErrRefreshTokenFailed(r.json()['error'])
            except ValueError:
                raise self.ErrRefreshTokenFailed(str(e))
        return r.json()

    # Logs in using Facebook access token
    def facebook_login(self, access_token):
        r = requests.post(
            self.hostname + '/v1/facebook/login',
            auth=(self.client_id, self.client_secret),
            data={
                'access_token': access_token,
                'scope': self.scope,
            },
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.ErrFacebookLoginFailed(r.json()['error'])
            except ValueError:
                raise self.ErrFacebookLoginFailed(str(e))
        return r.json()


def store_access_token(request, access_token):
    request.session['access_token'] = access_token
    request.session['access_token_granted_at'] = time()


def store_access_token_and_redirect(request, access_token):
    store_access_token(request=request, access_token=access_token)
    return redirect(settings.AFTER_LOGIN_VIEW)