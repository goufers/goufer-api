release: python manage.py migrate
web: gunicorn goufer.wsgi
worker: celery -A goufer worker
beat: celery -A goufer beat
