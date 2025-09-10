#!/bin/bash

echo "Starting entrypoint script..."

rm -rf static && ln -s /static static
rm -rf media && ln -s /media media
rm -rf logs && ln -s /logs logs

# Ждем, пока PostgreSQL станет доступен (если используется)
if [ "$ENGINE" = "django.db.backends.postgresql" ]; then
    echo "Waiting for PostgreSQL to become available..."
    export PGPASSWORD=$POSTGRES_PASSWORD
    until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
        >&2 echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done
    echo "PostgreSQL is up - continuing"
fi

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py load_initial_data
python manage.py ceate_superuser -u $ADMIN_USERNAME -e $ADMIN_EMAIL -p $ADMIN_PASSWORD 

echo "Starting Supervisor..."
exec /usr/bin/supervisord -c /opt/app/supervisor/supervisord.conf --nodaemon
