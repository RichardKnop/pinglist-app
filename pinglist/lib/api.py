from __future__ import absolute_import

import requests
import logging

logger = logging.getLogger(__name__)


class API(object):

    class APIError(Exception):
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
        logger.debug(r)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.APIError(r.json()['error'])
            except ValueError:
                raise self.APIError(str(e))
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
        logger.debug(r)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.APIError(r.json()['error'])
            except ValueError:
                raise self.APIError(str(e))
        return r.json()

    # Logs in using Facebook access token
    def facebook_login(self, fb_access_token):
        r = requests.post(
            self.hostname + '/v1/facebook/login',
            auth=(self.client_id, self.client_secret),
            data={
                'access_token': fb_access_token,
                'scope': self.scope,
            },
        )
        logger.debug(r)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.APIError(r.json()['error'])
            except ValueError:
                raise self.APIError(str(e))
        return r.json()

    # List plans
    def list_plans(self):
        r = requests.get(
            self.hostname + '/v1/plans',
            auth=(self.client_id, self.client_secret),
        )
        logger.debug(r)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.APIError(r.json()['error'])
            except ValueError:
                raise self.APIError(str(e))
        return r.json()

    # List subscriptions
    def list_subscriptions(self, access_token, user_id):
        r = requests.get(
            self.hostname + '/v1/subscriptions',
            headers={'Authorization': 'Bearer {}'.format(access_token)},
            params={'user_id': user_id},
        )
        logger.debug(r)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.APIError(r.json()['error'])
            except ValueError:
                raise self.APIError(str(e))
        return r.json()

    # List cards
    def list_cards(self, access_token, user_id):
        r = requests.get(
            self.hostname + '/v1/cards',
            headers={'Authorization': 'Bearer {}'.format(access_token)},
            params={'user_id': user_id},
        )
        logger.debug(r)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.APIError(r.json()['error'])
            except ValueError:
                raise self.APIError(str(e))
        return r.json()

    # Add a card
    def add_card(self, access_token, token):
        r = requests.post(
            self.hostname + '/v1/cards',
            headers={'Authorization': 'Bearer {}'.format(access_token)},
            json={
                'token': token,
            },
        )
        logger.debug(r)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.APIError(r.json()['error'])
            except ValueError:
                raise self.APIError(str(e))
        return r.json()

    # Get a card
    def get_card(self, access_token, card_id):
        r = requests.get(
            self.hostname + '/v1/cards/{}'.format(card_id),
            headers={'Authorization': 'Bearer {}'.format(access_token)},
        )
        logger.debug(r)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.APIError(r.json()['error'])
            except ValueError:
                raise self.APIError(str(e))
        return r.json()

    # Delete a card
    def delete_card(self, access_token, card_id):
        r = requests.delete(
            self.hostname + '/v1/cards/{}'.format(card_id),
            headers={'Authorization': 'Bearer {}'.format(access_token)},
        )
        logger.debug(r)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                raise self.APIError(r.json()['error'])
            except ValueError:
                raise self.APIError(str(e))