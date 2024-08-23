release: python manage.py migrate
web: gunicorn goufer.wsgi
worker: celery -A goufer worker -l INFO
beat: celery -A goufer beat -l INFO
