FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput --settings=config.settings

EXPOSE 8000

CMD python manage.py fix_db_state && \
    python manage.py migrate --noinput && \
    python manage.py create_admin && \
    python manage.py seed_tests && \
    gunicorn config.wsgi --workers 2 --threads 2 --timeout 60 --bind 0.0.0.0:8000
