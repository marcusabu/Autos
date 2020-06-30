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

        #Auto.objects.filter(bron='autoscout').delete()

        while next_page:
            page = requests.get(next_page)
            soup = BeautifulSoup(page.text, 'html.parser')

            listings = soup.find_all('div', class_='cl-list-element')
            if len(listings) > 1:
                for listing in listings:
                    if not listing.find('a'):
                        continue
                    listing_url = AUTOSCOUT_URL + listing.find('a')['href']
                    if not listing_url:
                        print("Listing link not found")
                        break

                    listing_page = requests.get(listing_url)
                    listing_soup = BeautifulSoup(listing_page.text, 'html.parser')

                    titel = listing_soup.find('h1', class_='cldt-detail-title').text.replace('\n', '')
                    prijs = int(re.sub("[^0-9]", "", listing_soup.find('div', class_='cldt-price').text.strip()))

                    try:
                        ad_url = listing_soup.find('a', class_='fed-finnik-link fed-data-url').get('data-url')
                    except Exception as e:
                        print("Cant find kenteken for ", listing_url)
                        continue
                    kenteken = re.search(r'kenteken/.+/', ad_url).group().split('/')[1]
                    kenteken = re.sub("[^0-9a-zA-Z]", "", kenteken)

                    auto = Auto(url=listing_url, titel=titel, bron='autoscout', kenteken=kenteken, prijs=prijs)

                    for feature in listing_soup.find_all('span', class_='cldt-stage-primary-keyfact'):
                        value = feature.text

                        if "km" in value:
                            auto.kilometer_stand = int(re.sub("[^0-9]", "", value))
                        if "/" in value: # Since 05/2013 string
                            auto.bouwjaar = int(value.split('/')[1])
                        if "PK" in value:
                            auto.vermogen = int(re.sub("[^0-9]", "", value))

                    for feature in listing_soup.find_all('dl'):
                        key = feature.find('dt').text
                        value = feature.find('dd').text

                        if 'Categorie' in key:
                            if len(feature.find_all('dd')) > 1:
                                auto.apk = dateparser.parse(feature.find_all('dd')[1].text.strip())
                        if "Transmissie" in key:
                            auto.is_handgeschakeld = bool("Handgeschakeld" in value)
                        if "Brandstof" in key:
                            auto.is_benzine = bool("Benzine" in value)

                    if auto.kenteken:
                        try:
                            auto.save()
                            print("Saved: ", auto.titel)
                        except IntegrityError as e:
                            print("Kenteken {} already in database, skipping...".format(auto.kenteken))
            else:
                print("No more listings found at ", next_page)

            # Regex magic to increment page
            next_page = re.sub(r'page=\d',
                               lambda exp: "page={}".format(int(re.sub("[^0-9]", "", exp.group(0))) + 1),
                               next_page)
            print(next_page, '\n\n')
