[![Codeship Status for RichardKnop/pinglist-app](https://codeship.com/projects/bdb716b0-de18-0133-2702-6a683e002de2/status?branch=master)](https://codeship.com/projects/144590)

[![Donate Bitcoin](https://img.shields.io/badge/donate-bitcoin-orange.svg)](https://richardknop.github.io/donate/)

# pinglist-app

API / website uptime & performance monitoring platform.

See also:
- [pinglist-api](https://github.com/RichardKnop/pinglist-api)
- [pinglist-ios-app](https://github.com/RichardKnop/pinglist-ios-app)

# Index

* [Pinglist App](#pinglist-app)
* [Index](#index)
* [Dependencies](#dependencies)
* [Setup](#setup)
* [Docker](#docker)
* [Releasing](#releasing)
* [Assets](#assets)

# Dependencies

Create a new virtual environment and install dependencies via pip:

```
virtualenv .venv
source .venv/bin/activate
pip install -r pinglist/requirements.txt
```

# Setup

If you are developing on OSX, install `etcd`, `Postgres`:

```
brew install etcd
brew install postgres
```

You might want to create a `Postgres` database:

```
createuser --createdb pinglist_app
createdb -U pinglist_app pinglist_app
```

Load a development configuration into `etcd`:

```
curl -L http://localhost:2379/v2/keys/config/pinglist_app.json -XPUT -d value='{
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
        "IOSLink": "#"
    },
    "IsDevelopment": true
}'
```

Run migrations:

```
python pinglist/manage.py migrate
```

And finally, run the app:

```
python pinglist/manage.py runserver
```

When deploying, you can set `ETCD_HOST` and `ETCD_PORT` environment variables.

# Docker

Build a Docker image and run the app in a container:

```
docker build -t pinglist-app .
docker run -e ETCD_HOST=localhost -e ETCD_PORT=2379 -p 6060:8080 pinglist-app
```

# Releasing

First, cut a release using `cut-release.sh` script. If you make a mistake, you can re-run the script as it will force push tags.

```
./cut-release.sh v0.0.0 --no-dry-run
```

Second, build a release using `build-release.sh` script. It will build a Docker image, tag it and push it to S3 bucket bucket. It might take a while depending on your connection speed as gzipped image is about 270MB.

```
./build-release.sh v0.0.0 --no-dry-run
```

# Assets

To upload assets to S3, do something along the lines:

```
python myarea/manage.py collectstatic --noinput
```

Or, alternatively:

```
aws s3 sync pinglist/proj/static/ s3://prod.pinglist.assets/pinglist-app/
```
