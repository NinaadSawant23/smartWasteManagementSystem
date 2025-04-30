# create_admin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swms.settings')  # Replace with your settings module
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "team7")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "giteshvs07@gmail.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "team7")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
