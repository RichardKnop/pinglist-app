# Set the base image to use to Ubuntu
FROM ubuntu:16.04

# Copy application source code
COPY . /srv/pinglist-app

# Update the default application repository sources list
RUN apt-get update

# Install needed packages
RUN apt-get install -y libpq-dev python python-dev python-pip nginx

# Configure nginx
RUN systemctl stop nginx
RUN ufw allow 'Nginx HTTP' # firewall profile
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /var/lib/nginx
RUN rm /etc/nginx/sites-enabled/default
ADD nginx/sites-enabled/ /etc/nginx/sites-enabled
RUN systemctl start nginx

# Create application subdirectories
WORKDIR /srv
RUN mkdir static logs

# Using the VOLUME command we makes directories available to other containers
VOLUME ["/srv/static/", "/srv/logs/"]

# Install Python dependencies
WORKDIR /srv/pinglist-app/pinglist
RUN pip install -r requirements.txt

# Copy the docker-entrypoint.sh script and use it as entrypoint
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

# Document that the service listens on port 8080.
EXPOSE 8080