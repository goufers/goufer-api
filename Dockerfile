
FROM python:3.12.4-alpine


# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# # set the working directory to /app
WORKDIR /app


RUN apk update && apk upgrade

# # sometimes the ownership of the files in the working directory is changed to root
# # and thus the app can't access the files and throws an error -> EACCES: permission denied
# # to avoid this, change the ownership of the files to the root user
# # USER root
# USER root


RUN apk add python3-dev \
           gcc \
           mysql-client \
           mysql-dev  \
           && pip install --upgrade pip

# RUN apk add --no-cache \
#          default-libmysqlclient-dev \
#          gcc \
#          build-base \
#          mysql-client \
#          mysql-dev \
#          && pip install --upgrade pip \
#          && apk del build-base



# RUN pip install pipenv

# RUN addgroup app && adduser -S -G app app

# USER app

# # change the ownership of the /app directory to the app user
# # chown -R <user>:<group> <directory>
# # chown command changes the user and/or group ownership of for given file.

# # Install application dependencies
# COPY Pipfile Pipfile.lock /app/

# COPY ./requirements.txt /requirements.txt

# RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers

# RUN pip install -r /requirements.txt

# RUN apk del .tmp

# # RUN mkdir -p /vol/web/media/

# # RUN mkdir -p /vol/web/media/

# # We use the --system flag so packages are installed into the system python
# # and not into a virtualenv. Docker containers don't need virtual environments. 
# RUN pipenv install --system --dev

# RUN chown -R app:app .

# # change the user back to the app user
# USER app

# # Copy the source code into the container's working directory
# COPY . .

# # expose port 8000 to tell Docker that the container listens on the specified network ports at runtime
# EXPOSE 8000


# command to run the app
# # CMD [ "python", "manage.py", "runserver" ]  
















