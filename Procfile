web: gunicorn fs_portfolio.wsgi --log-file -
release: python manage.py tailwind build && python manage.py makemigrations && python manage.py migrate