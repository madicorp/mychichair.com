import os

from django.core.management import BaseCommand

from mychichair.userprofile.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(admin_email, os.getenv('ADMIN_PASSWORD', 'changeme'))
