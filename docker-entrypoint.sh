#!/bin/bash

# Run database migrations
python manage.py migrate

# Collect the static files
python manage.py collectstatic --noinput

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

# Start Gunicorn processes in the background
exec gunicorn proj.wsgi:application \
    --name pinglist_app \
    --daemon \
    --bind unix:/tmp/gunicorn.sock \
    --workers 3 \
    --log-level=debug \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log

# And run the nginx server
/usr/sbin/nginx