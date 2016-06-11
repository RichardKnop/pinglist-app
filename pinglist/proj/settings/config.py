import os
import etcd
import json
import logging


logger = logging.getLogger('django')


# Let's start with some common sense default values
default_cnf = {
    "Database": {
        "Engine": "django.db.backends.postgresql_psycopg2",
        "Host": "localhost",
        "Port": 5432,
        "User": "pinglist_app",
        "Password": "",
        "DatabaseName": "pinglist_app"
    },
    "Oauth": {
        "ClientID": "test_client_1",
        "Secret": "test_secret"
    },
    "Django": {
        "Secret": "test_secret",
        "StaticStorage": "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
    "AWS": {
        "Region": "us-west-2",
        "AssetsBucket": "prod.pinglist.assets"
    },
    "Facebook": {
        "AppID": "facebook_app_id",
        "AppSecret": "facebook_app_secret"
    },
    "Stripe": {
        "PublishableKey": "stripe_publishable_key"
    },
    "Web": {
        "Scheme": "http",
        "Host": "localhost:8000",
        "APIScheme": "http",
        "APIHost": "localhost:8080"
    },
    "Pinglist": {
        "IOSLink": "https://itunes.apple.com/us/app/pinglist/id1114451352?ls=1&mt=8"
    },
    "IsDevelopment": True
}


def load_config():
    etcd_client = etcd.Client(
        host=os.getenv('ETCD_HOST', 'localhost'),
        port=int(os.getenv('ETCD_PORT', '2379')),
    )

    cnf = default_cnf.copy()

    # Try to load the remote config from etcd
    try:
        json_cnf = etcd_client.read('/config/pinglist_app.json').value
        new_cnf = json.loads(json_cnf)
        for k, v in new_cnf.iteritems():
            if k not in cnf:
                continue
            if isinstance(v, dict):
                for k2, v2 in v.iteritems():
                    if k2 in cnf[k]:
                        cnf[k][k2] = v2
            else:
                cnf[k] = v
    except (etcd.EtcdKeyNotFound, etcd.EtcdConnectionFailed) as e:
        logger.debug(str(e))
    except ValueError as e:
        logger.debug(json_cnf)

    return cnf
