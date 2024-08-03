from .common import *
import os
import dj_database_url




SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['goufer-616dedbb12a3.herokuapp.com']


DATABASES = {
    'default': dj_database_url.config()
}

CELERY_BROKER_URL = os.environ.get('REDIS_URL')




EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
