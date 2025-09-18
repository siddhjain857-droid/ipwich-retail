#!/usr/bin/env sh
set -e

# optional: wait for a DB if you later switch to Postgres
# python manage.py wait_for_db

echo "Applying migrations…"
python manage.py migrate --noinput

# optional but handy for PoC: collect static (safe even if already done)
python manage.py collectstatic --noinput

echo "Starting Gunicorn…"
exec gunicorn retail.wsgi:application --bind 0.0.0.0:8000
