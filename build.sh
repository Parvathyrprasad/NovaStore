
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ['DJANGO_SUPERUSER_USERNAME']

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=os.environ['DJANGO_SUPERUSER_EMAIL'],
        password=os.environ['DJANGO_SUPERUSER_PASSWORD']
    )
    print('Initial admin account created.')
else:
    print('Admin account already exists; no changes made.')
"
fi
