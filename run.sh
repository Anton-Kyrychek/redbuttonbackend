#!/bin/sh
sleep 10
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py loaddata alarmbutton/fixtures/fixtures.json
echo "from alarmbutton.models import Users; Users.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell

/usr/bin/tini -- /usr/sbin/nginx -c /etc/nginx-config &

/usr/bin/tini -- /usr/local/bin/gunicorn alarmbutton_backend.wsgi:application --workers=2 --threads=10 --bind=unix:/tmp/wsgi.sock --timeout=300
