from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
import re
from scraper.models import *
import dateparser
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Scrapes autotrack'

    def handle(self, *args, **options):
        # Base url includes 'airco' keyword
        AUTOTRACK_URL = 'https://www.autotrack.nl'
        BASE_URL = 'https://www.autotrack.nl/aanbod?merkIds=4f2f74d0-7812-416b-987f-210f9b3f5549&modelIds=4f318d5e-6f1a-4cf1-ba98-3677f529ac59&minimumprijs=&maximumprijs=&minimumbouwjaar=2007&zoekoptieIds=99ee096c-249b-4c50-ae4e-90653b1b58f5&paginagrootte=30&paginanummer=1'

        Auto.objects.filter(bron='autotrack').delete()

        next_page = BASE_URL

        while next_page:
            page = requests.get(next_page)
            soup = BeautifulSoup(page.text, 'html.parser')

            for listing in soup.find_all('li', class_='result-list-item'):
                listing_url = AUTOTRACK_URL + listing.find('a')['href']
                if not listing_url:
                    print("Listing link not found")
                    break

                listing_page = requests.get(listing_url)
                listing_soup = BeautifulSoup(listing_page.text, 'html.parser')

                titel = listing_soup.find('h1', class_='vdp__header__title').text + " " + listing_soup.find('h2', class_='vdp__header__subtitle').text

                auto = Auto(url=listing_url, titel=titel, bron='autotrack')
                try:
                    auto.prijs = int(listing.find('data', class_='result-item__price')['value'])
                except Exception as e:
                    print("Couldn't find price for {}".format(listing_url))
                    break
                auto.bouwjaar = int(listing.find('span', class_='result-item__date').text)
                auto.kilometer_stand = int(re.sub("[^0-9]", "", listing.find('span', class_='result-item__mileage').text))

                for feature in listing.find_all('button', class_='result-item__tag'):
                    if "PK" in feature.text:
                        pk = re.search('\(\d+\s..\)', feature.text).group()
                        auto.vermogen = int(re.sub("[^0-9]", "", pk))

                for feature in listing_soup.find_all('div', class_='vdp__usp__inner'):
                    key = feature.find('span').text
                    value = feature.contents[-1]

                    if "Transmissietype" in key:
                        auto.is_handgeschakeld = bool("Handgeschakeld" in value)
                    if "Brandstof" in key:
                        auto.is_benzine = bool("Benzine" in value)
                    if "Vermogen" in key:
                        auto.vermogen = int(re.sub("[^0-9]", "", value))
                    if "Kenteken" in key:
                        auto.kenteken = str(value)

                if auto.kenteken:
                    try:
                        auto.save()
                        print("Saved: ", auto.titel)
                    except IntegrityError as e:
                        print("Kenteken {} already in database, skipping...".format(auto.kenteken))


            # Regex magic to increment page
            next_page = re.sub(r'paginanummer=\d', lambda exp: "paginanummer={}".format(int(re.sub("[^0-9]", "", exp.group(0))) + 1), next_page)
            print(next_page, '\n\n')
