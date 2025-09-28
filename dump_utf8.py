import os
import django
from django.core.management import call_command

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_commerce.settings')
django.setup()  # Initialize Django

# Dump data to UTF-8 JSON
with open('data.json', 'w', encoding='utf-8') as f:
    call_command(
        'dumpdata',
        exclude=['auth.permission', 'contenttypes', 'authtoken.token'],
        indent=2,
        stdout=f
    )
