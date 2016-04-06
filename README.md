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
