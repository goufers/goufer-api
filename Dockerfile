FROM python:3.12.4-alpine 


# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# # set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache \
    python3-dev \
    build-base \
    mysql-client \
    mysql-dev \
    postgresql-dev \
    libffi-dev \
    gcc \
    musl-dev

RUN pip install --upgrade pip 

COPY Pipfile Pipfile.lock /app/

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN addgroup app && adduser -S -G app app

# set the user to run the app
USER app

# Expose port 8000 on the container
EXPOSE 8000