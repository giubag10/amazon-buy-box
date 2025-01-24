import unittest
from parameterized import parameterized
from data_extraction.scripts.amazon_scraper import extract_page_html


# Da lanciare con workspace la cartella tests mentre bisogna cambiare localmente gli import in data_extraction.scripts.*
class TestSequence(unittest.TestCase):
    @parameterized.expand([
        ["PORTA CELLULARE AUTO", "https://www.amazon.it/dp/B0C273FR2T/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["CUFFIE GAMING", "https://www.amazon.it/dp/B09DPSFBKF/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["TELECAMERA", "https://www.amazon.it/dp/B07XLML2YS/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["CAPSULE CAFFE'", "https://www.amazon.it/dp/B073VM19T8/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["INTEGRATORE ALIMENTARE", "https://www.amazon.it/dp/B07Q7WZ5R2/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["SCHEDA MICRO SD", "https://www.amazon.it/dp/B07YGZQ4H8/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["INSETTICIDA", "https://www.amazon.it/dp/B088B5H3KH/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["FORNO PIZZA", "https://www.amazon.it/dp/B0716ZNRR8/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["DISPOSITIVO ANTIABBANDONO", "https://www.amazon.it/dp/B078W8BBFK/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["LAMPADINE", "https://www.amazon.it/dp/B000UXA6AQ/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["GUANTI", "https://www.amazon.it/dp/B00FFY9KE8/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["CUBO DI RUBIK", "https://www.amazon.it/dp/B00HDZHREW/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"],
        ["INSETTICIDA 2", "https://www.amazon.it/dp/B09TWCFYXM/ref=olp-opf-redir?aod=1&ie=UTF8&condition=NEW"]
    ])
    def test_sequence(self, name, url):
        bs = extract_page_html(url)
        # C'è il buybox winner
        self.assertNotEqual(bs.find("div", {"id", "aod-pinned-offer"}), None)
        # Ci sono altri venditori
        self.assertNotEqual(bs.find("div", {"id": "aod-offer-list"}), None)
        self.assertNotEqual(bs.find_all("div", {"id": "aod-offer"}), None)
        self.assertTrue(len(bs.find_all("div", {"id": "aod-offer"})) > 1)
