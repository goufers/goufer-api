from .common import *

load_dotenv()


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+p*dvp7+2g2n2u-6ahklub4fvyvuy!@-q1qgf@$mx(dar6b(hb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


    
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'goufer_db',
        'USER': os.getenv('MY_SQL_HOST_USER'),
        'PASSWORD': os.getenv('MY_SQL_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}




EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

CELERY_BROKER_URL = 'redis://localhost:6379/1'

