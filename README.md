[![Codeship Status for RichardKnop/pinglist-app](https://codeship.com/projects/bdb716b0-de18-0133-2702-6a683e002de2/status?branch=master)](https://codeship.com/projects/144590)

# Pinglist App

Quick development setup:

```
createuser --createdb pinglist_app
createdb -U pinglist_app pinglist_app
cp pinglist/proj/settings/local.example.py pinglist/proj/settings/local.py
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python pinglist/manage.py migrate
python pinglist/manage.py runserver
```
