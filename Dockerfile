# Set the base image to use to Ubuntu 16.04 LTS
FROM ubuntu:16.04

# Copy application source code
COPY . /srv/pinglist-app

# Update the sources list
RUN apt-get update

# Install needed packages
RUN apt-get install -y libpq-dev python python-dev python-pip nginx

# Configure nginx
RUN ufw allow 'Nginx HTTP' # firewall profile
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /var/lib/nginx
RUN rm /etc/nginx/sites-enabled/default
ADD nginx/sites-enabled/ /etc/nginx/sites-enabled
RUN service reload nginx

# Create application subdirectories
WORKDIR /srv
RUN mkdir static logs

# Using the VOLUME command we makes directories available to other containers
VOLUME ["/srv/static/", "/srv/logs/"]

# Install Python dependencies
WORKDIR /srv/pinglist-app/pinglist
RUN pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Collect the static files
python manage.py collectstatic --noinput

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

# Start Gunicorn processes
exec gunicorn proj.wsgi:application \
    --name pinglist_app \
    --daemon \
    --bind unix:/tmp/gunicorn.sock \
    --workers 3 \
    --log-level=debug \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log

# Document that the service listens on port 80
EXPOSE 80