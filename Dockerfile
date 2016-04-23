# Set the base image to use to Ubuntu
FROM ubuntu:14.04

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV PINGLIST_SRC=pinglist
# Directory in container for all project files
ENV PINGLIST_SRVHOME=/srv
# Directory in container for project source files
ENV PINGLIST_SRVPROJ=/srv/pinglist

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python python-pip

# Create application subdirectories
WORKDIR $PINGLIST_SRVHOME
RUN mkdir media static logs
VOLUME ["$PINGLIST_SRVHOME/media/", "$PINGLIST_SRVHOME/logs/"]

# Copy application source code
COPY $PINGLIST_SRC $PINGLIST_SRVPROJ

# Install Python dependencies
RUN pip install -r $PINGLIST_SRVPROJ/requirements.txt

# Copy the docker-entrypoint.sh script and use it as entrypoint
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

# Document that the service listens on port 8080.
EXPOSE 8080