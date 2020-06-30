from django.core.management.base import BaseCommand
import re
from scraper.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        for auto in Auto.objects.all():
            auto.kenteken = re.sub("[^0-9a-zA-Z]", "", auto.kenteken)
            try:
                auto.save()
            except Exception as e:
                print(str(e))
                auto.delete()
