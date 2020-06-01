from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
import re
from scraper.models import *
import dateparser
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Scrapes autoscout'

    def handle(self, *args, **options):
        # Base url includes 'airco' keyword
        AUTOSCOUT_URL = 'https://www.autoscout24.nl'
        BASE_URL = 'https://www.autoscout24.nl/lst/fiat?sort=standard&desc=0&ustate=N%2CU&size=20&page=1&cy=NL&version0=punto&fregfrom=2007&atype=C&'

        next_page = BASE_URL

        while next_page:
            page = requests.get(next_page)
            soup = BeautifulSoup(page.text, 'html.parser')

            for listing in soup.find_all('div', class_='cl-list-element'):
                listing_url = AUTOSCOUT_URL + listing.find('a')['href']
                if not listing_url:
                    print("Listing link not found")
                    break

                listing_page = requests.get(listing_url)
                listing_soup = BeautifulSoup(listing_page.text, 'html.parser')

                titel = listing_soup.find('h1', class_='cldt-detail-title').text.replace('\n', '')

                date_string = listing_soup.find('span', id='displayed-since').find_all('span')[-1].text
                date = dateparser.parse(date_string)
                auto = Auto(url=listing_url, titel=titel, upload_datum=date, bron='marktplaats')

                for feature in listing_soup.find_all('div', class_='spec-table-item'):
                    key = feature.find('span', class_='key').text
                    value = feature.find('span', class_='value').text

                    if "Kilometerstand" in key:
                        auto.kilometer_stand = int(re.sub("[^0-9]", "", value))
                    if "Prijs" in key:
                        try:
                            auto.prijs = int(int(re.sub("[^0-9]", "", value)) / 100)
                        except Exception:
                            print("Couldn't parse value: ", value)
                    if "Transmissie" in key:
                        auto.is_handgeschakeld = bool("Handgeschakeld" in value)
                    if "Bouwjaar" in key:
                        auto.bouwjaar = int(value)
                    if "Brandstof" in key:
                        auto.is_benzine = bool("Benzine" in value)
                    if "Vermogen" in key:
                        auto.vermogen = int(re.sub("[^0-9]", "", value))
                    if "Kenteken" in key:
                        auto.kenteken = value

                if auto.kenteken:
                    try:
                        auto.save()
                        print("Saved: ", auto.titel)
                    except IntegrityError as e:
                        print("Kenteken {} already in database, skipping...".format(auto.kenteken))


            # Regex magic to increment page
            next_page = re.sub(r'\/p\/\d\/', lambda exp: "/p/{}/".format(int(re.sub("[^0-9]", "", exp.group(0))) + 1), next_page)
            print(next_page, '\n\n')
