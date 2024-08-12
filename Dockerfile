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

ENV SECRET_KEY ='django-insecure-+p*dvp7+2g2n2u-6ahklub4fvyvuy!@-q1qgf@$mx(dar6b(hb'
ENV account_sid ='AC937c61635a10f65f9b650cf217183884' 
ENV service_sid='VAff9f2f3279b1fc3d33fbc77d4a573f9d'
ENV auth_token='d7b4fe1e71ab31aa3ff7c895afd15d9e'
ENV EMAIL_HOST_USER='jamesezekiel039@gmail.com'
ENV EMAIL_HOST_PASSWORD='wfhi ndom udcd mtrb'
ENV DEFAULT_FROM_EMAIL='jamesezekiel039@gmail.com'

RUN addgroup app && adduser -S -G app app

RUN chown -R app:app .

USER app

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
