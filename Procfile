release: python manage.py migrate
web: gunicorn goufer.wsgi
beat: celery -A goufer beat