# Set the base image to use to Ubuntu
FROM ubuntu:16.04

# Update the default application repository sources list
RUN add-apt-repository -y ppa:nginx/stable
RUN apt-get update && apt-get -y upgrade

# Install needed packages
RUN apt-get install -y apt-utils
RUN apt-get install -y libpq-dev python-dev
RUN apt-get install -y python python-pip

# Install nginx
RUN apt-get install -y nginx

# Create application subdirectories
WORKDIR /srv
RUN mkdir static logs

# Using the VOLUME command we makes directories available to other containers
VOLUME ["/srv/static/", "/srv/logs/"]

# Copy application source code
COPY . /srv/pinglist-app

# Configure nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /var/lib/nginx
RUN rm /etc/nginx/sites-enabled/default
WORKDIR /srv/pinglist-app
RUN cp nginx.conf /etc/nginx/sites-enabled/default
RUN service nginx restart

# Install Python dependencies
WORKDIR /srv/pinglist-app/pinglist
RUN pip install -r requirements.txt

# Copy the docker-entrypoint.sh script and use it as entrypoint
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

# Document that the service listens on port 8080.
EXPOSE 8080