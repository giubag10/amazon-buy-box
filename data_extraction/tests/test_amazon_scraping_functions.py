from unittest import TestCase

from data_extraction.scripts.amazon_scraper import extract_page_html
from data_extraction.scripts.amazon_scraping_functions import get_seller_shipping_price, get_seller_name, \
    get_seller_avg_ratings, get_seller_flag_new, get_product_condition, get_price_element
from data_extraction.scripts.amazon_utils import check_amazon_seller


# Da lanciare con workspace la cartella tests mentre bisogna cambiare localmente gli import in data_extraction.scripts.*

class Test(TestCase):

    def test_get_element_price(self):
        bs = extract_page_html("https://www.amazon.it/dp/B0C94KNS8D/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW")
        buybox_root = bs.find("div", {"id", "aod-pinned-offer"})  # Vincitore buy box
        offer_list = bs.find_all("div", {"id": "aod-offer"})  # Altri venditori
        index = 0
        self.assertNotEqual(get_price_element(buybox_root, index), None)
        for offer in offer_list:
            index += 1
            self.assertNotEqual(get_price_element(offer, index), None)

    def test_get_seller_shipping_price(self):
        bs = extract_page_html("https://www.amazon.it/dp/B000UXA6AQ/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW")
        buybox_root = bs.find("div", {"id", "aod-pinned-offer"})  # Vincitore buy box
        offer_list = bs.find_all("div", {"id": "aod-offer"})  # Altri venditori
        self.assertNotEqual(get_seller_shipping_price(buybox_root), None)
        for offer in offer_list:
            self.assertNotEqual(get_seller_shipping_price(offer), None)

    def test_get_seller_name(self):
        bs = extract_page_html("https://www.amazon.it/dp/B00FFY9KE8/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW")
        buybox_root = bs.find("div", {"id", "aod-pinned-offer"})  # Vincitore buy box
        offer_list = bs.find_all("div", {"id": "aod-offer"})  # Altri venditori
        self.assertNotEqual(get_seller_name(buybox_root), None)
        for offer in offer_list:
            self.assertNotEqual(get_seller_name(offer), None)

    def test_get_seller_ratings_portacellulareauto(self):
        bs = extract_page_html("https://www.amazon.it/dp/B0C273FR2T/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW")
        buybox_root = bs.find("div", {"id", "aod-pinned-offer"})  # Vincitore buy box
        offer_list = bs.find_all("div", {"id": "aod-offer"})  # Altri venditori
        if not check_amazon_seller(get_seller_name(buybox_root).split()[0]):
            self.assertNotEqual(get_seller_avg_ratings(buybox_root), None)
        for offer in offer_list:
            if not check_amazon_seller(get_seller_name(offer).split()[0]):
                self.assertNotEqual(get_seller_avg_ratings(offer), None)

    def test_get_seller_ratings_telecamera(self):
        bs = extract_page_html("https://www.amazon.it/dp/B07XLML2YS/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW")
        buybox_root = bs.find("div", {"id", "aod-pinned-offer"})  # Vincitore buy box
        offer_list = bs.find_all("div", {"id": "aod-offer"})  # Altri venditori
        if not check_amazon_seller(get_seller_name(buybox_root).split()[0]):
            self.assertNotEqual(get_seller_avg_ratings(buybox_root), None)
        for offer in offer_list:
            # la verifica sul flag di nuovo venditore va messo dopo perchè è relazionato con il venditore amazon
            if not check_amazon_seller(get_seller_name(offer).split()[0]) and not get_seller_flag_new(offer):
                self.assertNotEqual(get_seller_avg_ratings(offer), None)

    def test_get_seller_flag_new_telecamera(self):
        bs = extract_page_html("https://www.amazon.it/dp/B07XLML2YS/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW")
        buybox_root = bs.find("div", {"id", "aod-pinned-offer"})  # Vincitore buy box
        offer_list = bs.find_all("div", {"id": "aod-offer"})  # Altri venditori
        if not check_amazon_seller(get_seller_name(buybox_root).split()[0]):
            self.assertNotEqual(get_seller_flag_new(buybox_root), None)
        for offer in offer_list:
            if not check_amazon_seller(get_seller_name(offer).split()[0]):
                self.assertNotEqual(get_seller_flag_new(offer), None)

    def test_get_seller_flag_new_caffe(self):
        bs = extract_page_html("https://www.amazon.it/dp/B01LQQQWG2/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW")
        buybox_root = bs.find("div", {"id", "aod-pinned-offer"})  # Vincitore buy box
        offer_list = bs.find_all("div", {"id": "aod-offer"})  # Altri venditori
        if not check_amazon_seller(get_seller_name(buybox_root).split()[0]):
            self.assertNotEqual(get_seller_flag_new(buybox_root), None)
        for offer in offer_list:
            if not check_amazon_seller(get_seller_name(offer).split()[0]):
                self.assertNotEqual(get_seller_flag_new(offer), None)

    def test_get_product_condition_caffe(self):
        bs = extract_page_html("https://www.amazon.it/dp/B01LQQQWG2/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW")
        buybox_root = bs.find("div", {"id", "aod-pinned-offer"})  # Vincitore buy box
        offer_list = bs.find_all("div", {"id": "aod-offer"})  # Altri venditori
        self.assertNotEqual(get_product_condition(buybox_root), None)
        for offer in offer_list:
            self.assertNotEqual(get_product_condition(offer), None)

    def test_get_seller_shipping_price_caffe(self):
        bs = extract_page_html("https://www.amazon.it/dp/B01LQQQWG2/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW")
        buybox_root = bs.find("div", {"id", "aod-pinned-offer"})  # Vincitore buy box
        offer_list = bs.find_all("div", {"id": "aod-offer"})  # Altri venditori
        self.assertNotEqual(get_seller_shipping_price(buybox_root), None)
        for offer in offer_list:
            self.assertNotEqual(get_seller_shipping_price(offer), None)
