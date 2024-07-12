# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/


FROM python:3.12.4-alpine3.20


# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1


# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1


# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
# create a user with permissions to run the app
# -S -> create a system user
# -G -> add the user to a group
# This is done to avoid running the app as root
# If the app is run as root, any vulnerability in the app can be exploited to gain access to the host system
# It's a good practice to run the app as a non-root user
RUN addgroup app && adduser -S -G app app

# Switch to the non-privileged user to run the application.
USER app

# set the working directory to /app
WORKDIR /app


# Required to install mysqlclient with Pip
RUN apt-get update \
  && apt-get install python3-dev default-libmysqlclient-dev gcc -y

# Install pipenv
RUN pip install --upgrade pip 
RUN pip install pipenv

# copy pipfile and pipfile.lock to the working directory
# This is done before copying the rest of the files to take advantage of Docker’s cache
# If the pipfile and pipfile.lock files haven’t changed, Docker will use the cached dependencies
COPY Pipfile Pipfile.lock /app/

# We use the --system flag so packages are installed into the system python
# and not into a virtualenv. Docker containers don't need virtual environments.
RUN pipenv install --system --dev

# sometimes the ownership of the files in the working directory is changed to root
# and thus the app can't access the files and throws an error -> EACCES: permission denied
# to avoid this, change the ownership of the files to the root user
USER root

# change the ownership of the /app directory to the app user
# chown -R <user>:<group> <directory>
# chown command changes the user and/or group ownership of for given file.
RUN chown -R app:app .

# change the user back to the app user
USER app

# Copy the source code into the container's working directory
COPY . .

# expose port 8000 to tell Docker that the container listens on the specified network ports at runtime
EXPOSE 8000

# command to run the app
CMD [ "python", "manage.py", "runserver" ]  