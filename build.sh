#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Automatically create or reset the admin superuser
python manage.py createsuperuser --noinput || python manage.py shell -c "
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if password:
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f'Successfully updated password for superuser {username}')
    except User.DoesNotExist:
        User.objects.create_superuser(username=username, email='', password=password)
        print(f'Successfully created superuser {username}')
"