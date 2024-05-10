#!/usr/bin/env bash
# Retrieve Superuser Email
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"authentication@service.com"}

# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Create Super User
python manage.py createsuperuser --username $SUPERUSER_EMAIL --email $SUPERUSER_EMAIL --noinput || true

