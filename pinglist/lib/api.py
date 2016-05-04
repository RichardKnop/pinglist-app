from __future__ import absolute_import

import requests
import logging

logger = logging.getLogger('django')


class API(object):
    class APIError(Exception):
        pass

    def __init__(self, hostname, client_id, client_secret, scope):
        self.hostname = hostname
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope

    # Registers a new user
    def register(self, username, password):
        r = requests.post(
            self.hostname + '/v1/accounts/users',
            auth=(self.client_id, self.client_secret),
            json={
                'email': username,
                'password': password,
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

    # Resets a user password
    def reset_password(self, email):
        r = requests.post(
            self.hostname + '/v1/accounts/password-reset',
            auth=(self.client_id, self.client_secret),
            json={
                'email': email,
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

    # List cards
    def list_cards(self, access_token, user_id, page):
        r = requests.get(
            self.hostname + '/v1/cards?page={}&order_by=id desc'.format(page),
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

    # List subscriptions
    def list_subscriptions(self, access_token, user_id, page):
        r = requests.get(
            self.hostname + '/v1/subscriptions?page={}&order_by=id desc'.format(page),
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

    # Add a subscription
    def add_subscription(self, access_token, plan_id):
        r = requests.post(
            self.hostname + '/v1/subscriptions',
            headers={'Authorization': 'Bearer {}'.format(access_token)},
            json={
                'plan_id': plan_id,
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

    # Get a subscription
    def get_subscription(self, access_token, subscription_id):
        r = requests.get(
            self.hostname + '/v1/subscriptions/{}'.format(subscription_id),
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

    # Update a subscription
    def update_subscription(self, access_token, subscription_id, plan_id):
        r = requests.put(
            self.hostname + '/v1/subscriptions/{}'.format(subscription_id),
            headers={'Authorization': 'Bearer {}'.format(access_token)},
            json={
                'plan_id': plan_id,
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

    # Cancel a subscription
    def cancel_subscription(self, access_token, subscription_id):
        r = requests.delete(
            self.hostname + '/v1/subscriptions/{}'.format(subscription_id),
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

    # Get a profile
    def get_profile(self, access_token):
        r = requests.get(
            self.hostname + '/v1/accounts/me',
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

    # Update a profile
    def update_profile(self, access_token, profile):
        r = requests.put(
            self.hostname + '/v1/accounts/users/{}'.format(profile['id']),
            headers={'Authorization': 'Bearer {}'.format(access_token)},
            json=profile,
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

    # List regions
    def list_regions(self, access_token):
        r = requests.get(
            self.hostname + '/v1/regions',
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

    # List alarms
    def list_alarms(self, access_token, user_id, page):
        r = requests.get(
            self.hostname + '/v1/alarms?page={}&order_by=id desc'.format(page),
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

    # Add an alarm
    def add_alarm(self, access_token, alarm):
        r = requests.post(
            self.hostname + '/v1/alarms',
            headers={'Authorization': 'Bearer {}'.format(access_token)},
            json=alarm,
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

    # Get an alarm
    def get_alarm(self, access_token, alarm_id):
        r = requests.get(
            self.hostname + '/v1/alarms/{}'.format(alarm_id),
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

    # Update an alarm
    def update_alarm(self, access_token, alarm):
        r = requests.put(
            self.hostname + '/v1/alarms/{}'.format(alarm['id']),
            headers={'Authorization': 'Bearer {}'.format(access_token)},
            json=alarm,
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

    # Delete an alarm
    def delete_alarm(self, access_token, alarm_id):
        r = requests.delete(
            self.hostname + '/v1/alarms/{}'.format(alarm_id),
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

    # List alarm incidents
    def list_alarm_incidents(self, access_token, alarm_id, page):
        r = requests.get(
            self.hostname + '/v1/alarms/{}/incidents?page={}&order_by=id desc'.format(alarm_id, page),
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

    # List alarm metrics
    def list_alarm_metrics(self, access_token, alarm_id, date_trunc, date_from, date_to):
        params = {k: v for k, v in {
            'date_trunc': date_trunc if date_trunc else None,
            'from': date_from.utcnow().isoformat() + 'Z' if date_from else None,
            'to': date_to.utcnow().isoformat() + 'Z' if date_to else None,
        }.iteritems() if v}
        r = requests.get(
            self.hostname + '/v1/alarms/{}/response-times?{}'.format(
                alarm_id,
                '&'.join(['{}={}'.format(k, v) for k, v in params.iteritems()]),
            ),
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

    # List teams
    def list_teams(self, access_token, user_id, page):
        r = requests.get(
            self.hostname + '/v1/teams?page={}&order_by=id desc'.format(page),
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

    # Add a team
    def add_team(self, access_token, team):
        r = requests.post(
            self.hostname + '/v1/teams',
            headers={'Authorization': 'Bearer {}'.format(access_token)},
            json=team,
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

    # Get a team
    def get_team(self, access_token, team_id):
        r = requests.get(
            self.hostname + '/v1/teams/{}'.format(team_id),
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

    # Update a team
    def update_team(self, access_token, team):
        r = requests.put(
            self.hostname + '/v1/teams/{}'.format(team['id']),
            headers={'Authorization': 'Bearer {}'.format(access_token)},
            json=team,
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

    # Delete a team
    def delete_team(self, access_token, team_id):
        r = requests.delete(
            self.hostname + '/v1/teams/{}'.format(team_id),
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

    # Send a contact email to the admin
    def contact(self, name, email, subject, message):
        r = requests.post(
            self.hostname + '/v1/accounts/contact',
            auth=(self.client_id, self.client_secret),
            json={
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
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
