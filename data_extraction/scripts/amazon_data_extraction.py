import datetime
import json
import os

import pandas as pd

from amazon_mongo import insert_scraping_json_list, select_products, insert_products_from_csv
from amazon_scraper import scrape_amazon
from logger import logging


def scrape_product(prod_row, dt_scraping):
    logging.info("Estrazione dati prodotto " + prod_row["name"])
    return {
        "name": prod_row["name"],
        "url": prod_row["link"],
        "datetime_extraction": dt_scraping.strftime("%Y-%m-%d %H:%M:%S"),
        "data": scrape_amazon(prod_row["link"])
    }


def read_products(products_csv_path):
    product_list_from_mongo = select_products()
    if product_list_from_mongo is None or len(product_list_from_mongo) == 0:
        # Inizialize products collection on MongoDB
        insert_products_from_csv(products_csv_path)
        products_df = pd.read_csv(products_csv_path)
    else:
        products_df = pd.DataFrame(product_list_from_mongo)

    return products_df


path_prodotti_csv = os.getenv("PATH_PRODOTTI_CSV", "../resources/prodotti.csv")
path_results = os.getenv("PATH_RESULTS", "../results")

df_prodotti = read_products(path_prodotti_csv)

datetime_extraction = datetime.datetime.now()
result_file_name = path_results + '/result' + datetime_extraction.strftime("%Y%m%d%H%M%S") + '.json'
result = []
logging.info("--- AMAZON SCRAPING " + datetime_extraction.strftime("%Y-%m-%d %H:%M:%S") + " ---")

for index, row in df_prodotti.iterrows():
    result.append(scrape_product(row, datetime_extraction))

if not os.path.exists(path_results):
    os.makedirs(path_results)
with open(result_file_name, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

insert_scraping_json_list(result)

