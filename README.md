[![Codeship Status for RichardKnop/pinglist-app](https://codeship.com/projects/bdb716b0-de18-0133-2702-6a683e002de2/status?branch=master)](https://codeship.com/projects/144590)

# Pinglist App

API / website uptime & performance monitoring platform.

# Index

* [Pinglist App](#pinglist-app)
* [Index](#index)
* [Dependencies](#dependencies)
* [Setup](#setup)
* [Docker](#docker)
* [Releasing](#releasing)
* [Assets](#assets)

# Dependencies

Create a mnew virtual environment and install dependencies via pip:

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
createuser --createdb pinglist_app_
createdb -U pinglist_app_ pinglist_app_
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
        "Secret": "test_secret"
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
    "IOSLink": "#",
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
s3cmd sync pinglist/proj/static/* s3://prod.pinglist.assets/
```