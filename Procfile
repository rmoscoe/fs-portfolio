release: python manage.py tailwind build && python manage.py migrate
web: gunicorn fs_portfolio.wsgi --log-file -