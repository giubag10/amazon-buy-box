import datetime
from logger import logging

mesi_italiano = {
    "gennaio": 1,
    "febbraio": 2,
    "marzo": 3,
    "aprile": 4,
    "maggio": 5,
    "giugno": 6,
    "luglio": 7,
    "agosto": 8,
    "settembre": 9,
    "ottobre": 10,
    "novembre": 11,
    "dicembre": 12
}

amazon_product_condition_dict = {
    "Nuovo": 5,
    "Usato - Come nuovo": 4,
    "Usato - Ottime condizioni": 3,
    "Usato - Buone condizioni": 2,
    "Usato - Condizioni accettabili": 1
}


def encode_product_condition(product_condition_text):
    return amazon_product_condition_dict[product_condition_text] \
        if product_condition_text in amazon_product_condition_dict \
        else amazon_product_condition_dict["Nuovo"]


def parse_date_text(date_text):
    try:
        day = int(date_text.split(" ")[0])
        month = int(mesi_italiano[date_text.split(" ")[1]])
        today_month = datetime.date.today().month
        if month >= today_month:
            year = datetime.date.today().year
        else:
            year = datetime.date.today().year + 1
        return datetime.date(year, month, day)
    except Exception as e:
        logging.error("Parsing date error!", e)
        return None


def check_amazon_seller(seller_name):
    # Gestisce Amazon, Amazon con spazi e AmazonFresh
    return "Amazon" in seller_name
