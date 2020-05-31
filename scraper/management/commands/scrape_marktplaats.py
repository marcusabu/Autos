from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
import requests
import re
from scraper.models import *
import dateparser


class Command(BaseCommand):
    help = 'Scrapes marktplaats'

    def handle(self, *args, **options):
        # Base url includes 'airco' keyword
        MARKTPLAATS_URL = 'https://www.marktplaats.nl'
        BASE_URL = 'https://www.marktplaats.nl/l/auto-s/fiat/f/grande-punto/772/p/1/#q:airco|f:10882,759,779|constructionYearFrom:2007|postcode:2333AS|searchInTitleAndDescription:true'
        URL_SUFFIX = '#q:airco|f:10882,779,772|constructionYearFrom:2007|postcode:2333AS|searchInTitleAndDescription:true'

        #Auto.objects.all().delete()

        next_page = BASE_URL

        while next_page:
            page = requests.get(next_page)
            soup = BeautifulSoup(page.text, 'html.parser')

            for listing in soup.find_all('li', class_='mp-Listing'):
                listing_url = MARKTPLAATS_URL + listing.find('a', class_='mp-Listing-coverLink')['href']
                if not listing_url:
                    print("Listing link not found")
                    break

                listing_page = requests.get(listing_url)
                listing_soup = BeautifulSoup(listing_page.text, 'html.parser')

                titel = listing_soup.find('h1', id='title').text

                date_string = listing_soup.find('span', id='displayed-since').find_all('span')[-1].text
                date = dateparser.parse(date_string)
                auto = Auto(url=listing_url, titel=titel, upload_datum=date)

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
                        auto.isHandgeschakeld = bool("Handgeschakeld" in value)
                    if "Bouwjaar" in key:
                        auto.bouwjaar = int(value)
                    if "Brandstof" in key:
                        auto.isBenzine = bool("Benzine" in value)
                    if "Vermogen" in key:
                        auto.vermogen = int(re.sub("[^0-9]", "", value))
                    if "Kenteken" in key:
                        auto.kenteken = value

                auto.save()
                print("Saved: ", auto.titel)

            # Regex magic to increment page
            next_page = re.sub(r'\/p\/\d\/', lambda exp: "/p/{}/".format(int(re.sub("[^0-9]", "", exp.group(0))) + 1), next_page)
            print(next_page)
