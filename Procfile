release: python manage.py migrate && python manage.py create_default_superuser && python manage.py collectstatic --noinput
web: gunicorn config.wsgi --log-file -
