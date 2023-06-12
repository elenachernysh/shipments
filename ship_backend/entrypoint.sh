#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z 'deliverymydb' 5432; do
  sleep 0.5
done

echo "PostgreSQL started"


python manage.py flush --no-input
python manage.py migrate

exec "$@"