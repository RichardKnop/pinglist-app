# Set the base image to use to Ubuntu
FROM ubuntu:16.04

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade

# Install needed packages
RUN apt-get install -y apt-utils
RUN apt-get install -y libpq-dev python-dev
RUN apt-get install -y python python-pip

# Install nginx
RUN apt-get install -y nginx

# Create application subdirectories
WORKDIR /srv
RUN mkdir media static logs

# Using the VOLUME command we makes directories available to other containers
VOLUME ["/srv/media/", "/srv/logs/"]

# Copy application source code
COPY . /srv/pinglist-app

# Configure nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN cat >/etc/nginx/sites-enabled/pinglist_app.conf <<EOL
upstream app_server {
    # fail_timeout=0 means we always retry an upstream even if it failed
    # to return a good HTTP response (in case the Unicorn master nukes a
    # single worker for timing out).

    server unix:/tmp/gunicorn.sock fail_timeout=0;
}

server {

    listen   8080;
    server_name .pingli.st;

    client_max_body_size 5M;

    location /static/ {
        alias   /srv/static/;
    }

    location / {
        # an HTTP header important enough to have its own Wikipedia entry:
        #   http://en.wikipedia.org/wiki/X-Forwarded-For
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # enable this if and only if you use HTTPS, this helps Rack
        # set the proper protocol for doing redirects:
        # proxy_set_header X-Forwarded-Proto https;

        # pass the Host: header from the client right along so redirects
        # can be set properly within the Rack application
        proxy_set_header Host $http_host;

        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;

        # set "proxy_buffering off" *only* for Rainbows! when doing
        # Comet/long-poll stuff.  It's also safe to set if you're
        # using only serving fast clients with Unicorn + nginx.
        # Otherwise you _want_ nginx to buffer responses to slow
        # clients, really.
        # proxy_buffering off;

        # Try to serve static files from nginx, no point in making an
        # *application* server like Unicorn/Rainbows! serve static files.
        if (!-f $request_filename) {
            proxy_pass http://app_server;
            break;
        }
    }

    # Error pages
    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root /srv/static/;
    }
}

EOL

# Install Python dependencies
WORKDIR /srv/pinglist-app/pinglist
RUN pip install -r requirements.txt

# Copy the docker-entrypoint.sh script and use it as entrypoint
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

# Document that the service listens on port 8080.
EXPOSE 8080