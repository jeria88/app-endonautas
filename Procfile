web: python manage.py fix_db_state && python manage.py migrate --noinput && gunicorn config.wsgi --workers 2 --threads 2 --timeout 60 --bind 0.0.0.0:$PORT
