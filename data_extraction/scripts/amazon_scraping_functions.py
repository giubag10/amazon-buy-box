import datetime
import re
from amazon_utils import encode_product_condition, parse_date_text, mesi_italiano, \
    check_amazon_seller
from logger import logging


def get_price_element(root, index):
    try:
        price_element = root.find("span", {"id": "aod-price-" + str(index)}) \
                            .find("span", {"class": "a-offscreen"}) \
                            .text[:-1].replace(',', '.')
        if price_element == '':
            price_whole = root.find("span", {"id": "aod-price-" + str(index)}) \
                            .find("span", {"class": "a-price-whole"}).text.replace(',', '.')
            price_fraction = root.find("span", {"id": "aod-price-" + str(index)}) \
                            .find("span", {"class": "a-price-fraction"}).text
            price_element = price_whole + price_fraction
        price_element = float(price_element)
    except AttributeError as e:
        logging.exception("Price element " + str(index) + " not found!")
        return None
    return price_element


def get_seller_name(root):
    try:
        seller_name_div = root.find("div", {"id": "aod-offer-soldBy"})
        seller_name_a = seller_name_div.find("a", {"class": "a-size-small a-link-normal"})
        if seller_name_a is not None:
            seller_name = seller_name_a.text.strip()
        else:
            seller_name = seller_name_div.find("span", {"class": "a-size-small a-color-base"}).text.strip()
    except AttributeError as e:
        logging.exception("Seller Name not found!")
        return None
    except Exception as e:
        logging.exception("Seller name parsing in exception!")
        return None
    return seller_name


def get_product_num_ratings(root):
    try:
        product_num_ratings = root.find("span", {"id": "aod-asin-reviews-count-title"}).text
        product_num_ratings = re.findall('[0-9]+.[0-9]+', product_num_ratings)[0]
        product_num_ratings = int(product_num_ratings.replace(".", ""))
    except AttributeError as e:
        logging.exception("Product Num Ratings not found!")
        return None
    except Exception as e:
        logging.exception("Product Num Ratings parsing in exception!")
        return None
    return product_num_ratings


def get_seller_flag_new(root):
    try:
        seller_flag_new_text = root.find("div", {"id": "aod-offer-seller-rating"}) \
            .find("span", {"id": "seller-rating-count-{iter}"}).text.strip()
        seller_flag_new = seller_flag_new_text == "Nuovo venditore"
    except AttributeError as e:
        logging.exception("Seller Flag New not found!")
        return None
    except Exception as e:
        logging.exception("Seller Flag New parsing in exception!")
        return None
    return seller_flag_new


def get_seller_avg_ratings(root):
    try:
        seller_avg_ratings = root.find("div", {"id": "aod-offer-seller-rating"}) \
            .find("i", {"class": "a-icon-star-mini"})
        seller_avg_ratings = re.findall('[0-9]-?[0-9]?', str(seller_avg_ratings))[0]
        seller_avg_ratings = float(seller_avg_ratings.replace('-', '.'))
    except AttributeError as e:
        logging.exception("Seller Average Ratings in stars not found!")
        return None
    except Exception as e:
        logging.exception("Seller Average Ratings in stars parsing in exception!")
        return None
    return seller_avg_ratings


def get_seller_perc_positive_ratings(root):
    try:
        seller_perc_positive_ratings = root.find("div", {"id": "aod-offer-seller-rating"}) \
            .find("span", {"id": "seller-rating-count-{iter}"})
        seller_perc_positive_ratings = re.findall('[0-9]+%', str(seller_perc_positive_ratings))[0]
        seller_perc_positive_ratings = int(seller_perc_positive_ratings.replace('%', ''))
    except AttributeError as e:
        logging.exception("Seller Percentage positive ratings not found!")
        return None
    except Exception as e:
        logging.exception("Seller Percentage positive ratings parsing in exception!")
        return None
    return seller_perc_positive_ratings


def get_seller_num_ratings(root):
    try:
        seller_num_ratings = root.find("div", {"id": "aod-offer-seller-rating"}) \
            .find("span", {"id": "seller-rating-count-{iter}"})
        seller_num_ratings = re.findall('[(]{1}[0-9]+ valutazion[e|i]{1}[)]{1}', str(seller_num_ratings))[0]
        seller_num_ratings = int(seller_num_ratings.replace('(', '')
                                 .replace(' valutazioni)', '')
                                 .replace(' valutazione)', ''))
    except AttributeError as e:
        logging.exception("Seller num ratings not found!")
        return None
    except Exception as e:
        logging.exception("Seller num ratings parsing in exception!")
        return None
    return seller_num_ratings


def get_product_name(root):
    try:
        product_name = root.find("h5", {"id": "aod-asin-title-text"}).text[1:]
    except AttributeError as e:
        logging.exception("Product name not found!")
        return None
    except Exception as e:
        logging.exception("Product name parsing in exception!")
        return None
    return product_name


def get_seller_shipping_price(root):
    try:
        seller_shipping_price_text = root.find("div", {"id": "mir-layout-DELIVERY_BLOCK"}).text
        if "GRATUITA" in seller_shipping_price_text or "Consegna senza costi aggiuntivi" in seller_shipping_price_text:
            seller_shipping_price = 0
        else:
            seller_shipping_price = float((re.findall('[0-9]+,?[0-9]*.*€', seller_shipping_price_text)[0][:-1].strip()) \
                                          .replace(',', '.'))
    except AttributeError as e:
        logging.exception("Seller Shipping price not found!")
        return None
    except Exception as e:
        logging.exception("Seller Shipping price parsing in exception!")
        return None
    return seller_shipping_price


def get_product_condition(root):
    try:
        product_condition = (root.find("div", {"id": "aod-offer-heading"})
                             # .h5  # Not parsable from 17/12/2024
                             .text.replace("\n", ""))
        product_condition = product_condition.strip()
        product_condition = encode_product_condition(product_condition)
    except AttributeError as e:
        logging.exception("Product condition not found!")
        return None
    except Exception as e:
        logging.exception("Product condition parsing in exception!")
        return None
    return product_condition


def get_seller_shipping_days(root):
    try:
        seller_shipping_days_text = root.find("div", {"id": "mir-layout-DELIVERY_BLOCK"}) \
            .find("span", {"class": "a-text-bold"}).text
        seller_shipping_days_text = re.findall('[0-9]+ [' + '|'.join(mesi_italiano.keys()) + ']+',
                                               seller_shipping_days_text)[0]
        seller_shipping_days_date = parse_date_text(seller_shipping_days_text)
        if seller_shipping_days_date is None:
            return None
        else:
            seller_shipping_days = (seller_shipping_days_date - datetime.date.today()).days
    except AttributeError as e:
        logging.exception("Seller Shipping days not found!")
        return None
    except Exception as e:
        logging.exception("Seller Shipping days parsing in exception!")
        return None
    return seller_shipping_days


def get_seller_fba(root):
    try:
        seller_fba = root.find("div", {"id": "aod-offer-shipsFrom"}) \
            .find("span", {"class": "a-size-small a-color-base"}).text
        seller_fba = check_amazon_seller(seller_fba.split()[0])
    except AttributeError as e:
        logging.exception("Seller FBA not found!")
        return None
    except Exception as e:
        logging.exception("Seller FBA parsing in exception!")
        return None
    return seller_fba


def get_seller_info(seller_root, index, buybox_seller_data):
    is_buy_box_seller = index == 0
    is_buy_box_absent = (is_buy_box_seller and "Nessuna offerta in evidenza disponibile" in seller_root.text) or (not is_buy_box_seller and buybox_seller_data is None)
    if is_buy_box_absent:
        logging.warning("Buy box seller is absent!")
        return None
    seller_name = get_seller_name(seller_root)
    is_seller_amazon = check_amazon_seller(seller_name.split()[0])
    is_new_seller = False if is_seller_amazon else get_seller_flag_new(seller_root)
    price_no_shipping = get_price_element(seller_root, index)
    seller_shipping_price = get_seller_shipping_price(seller_root)
    total_price = price_no_shipping + seller_shipping_price
    buybox_price_no_shipping = 0 if is_buy_box_seller or is_buy_box_absent else buybox_seller_data["sale"]["priceNoShipping"]
    buybox_shipping_price = 0 if is_buy_box_seller or is_buy_box_absent else buybox_seller_data["shipping"]["price"]
    buybox_total_price = 0 if is_buy_box_seller or is_buy_box_absent else buybox_seller_data["sale"]["totalPrice"]
    return {
        "name": seller_name,
        "index": index,
        "sale": {
            "priceNoShipping": price_no_shipping,
            "condition": get_product_condition(seller_root),
            "totalPrice": total_price,
            "diffPriceNoShipping": 0 if is_buy_box_seller or is_buy_box_absent else price_no_shipping - buybox_price_no_shipping,
            "diffTotalPrice": 0 if is_buy_box_seller or is_buy_box_absent else total_price - buybox_total_price,
        },
        "shipping": {
            "price": seller_shipping_price,
            "days": get_seller_shipping_days(seller_root),
            "diffPrice": 0 if is_buy_box_seller or is_buy_box_absent else seller_shipping_price - buybox_shipping_price,
        },
        "ratings": {
            "isNew": is_new_seller,
            "avg": None if is_seller_amazon or is_new_seller else get_seller_avg_ratings(seller_root),
            "num": None if is_seller_amazon or is_new_seller else get_seller_num_ratings(seller_root),
            "perc_positive": None if is_seller_amazon or is_new_seller else get_seller_perc_positive_ratings(seller_root)
        },
        "fba": True if is_seller_amazon else get_seller_fba(seller_root)
    }


def get_other_seller_info(seller_list, buybox_seller_data):
    other_sellers = []
    index = 1
    for offer_item in seller_list:
        logging.info("Seller " + str(index))
        other_sellers.append(get_seller_info(offer_item, index, buybox_seller_data))
        index += 1
    return other_sellers
