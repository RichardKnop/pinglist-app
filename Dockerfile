# Set the base image to use to Ubuntu
FROM ubuntu:16.04

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y apt-utils
RUN apt-get install -y libpq-dev python-dev
RUN apt-get install -y python python-pip

# Create application subdirectories
WORKDIR /srv
RUN mkdir media static logs
VOLUME ["/srv/media/", "/srv/logs/"]

# Copy application source code
COPY . /srv/pinglist-app

# Install Python dependencies
WORKDIR /srv/pinglist-app/pinglist
RUN pip install -r requirements.txt

# Copy the docker-entrypoint.sh script and use it as entrypoint
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

# Document that the service listens on port 8080.
EXPOSE 8080