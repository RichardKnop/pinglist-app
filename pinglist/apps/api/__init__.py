from __future__ import absolute_import

import requests


class API(object):

    class ErrLoginFailed(Exception):
        pass

    class ErrRefrestTokenFailed(Exception):
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
        if r.status_code != 200:
            raise self.ErrLoginFailed(r.json()['error'])
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
        if r.status_code != 200:
            raise self.ErrRefrestTokenFailed(r.json()['error'])
        return r.json()