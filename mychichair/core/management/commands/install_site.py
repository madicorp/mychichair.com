from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create mychichair django admin site in db'

    def handle(self, *args, **options):
        site_name = "mychichair"
        site_domain = settings.SITE_DOMAIN
        if not site_domain:
            site_domain = 'localhost:8000'
        if Site.objects.filter(pk=settings.SITE_ID).exists():
            site = Site.objects.get(
                pk=settings.SITE_ID
            )
            site.domain = site_domain
            site.name = site_name
        else:
            site = Site(pk=settings.SITE_ID, name=site_name, domain=site_domain)
        site.save()
