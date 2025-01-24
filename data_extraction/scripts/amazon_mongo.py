import pandas as pd
import pymongo
from pymongo.errors import DuplicateKeyError

from logger import logging

username = "root"
password = "amazon"
db_name = "mongodb"  # il nome dato al container Docker di MongoDB (localhost in locale)
# db_name = "localhost"  # DECOMMENTARE IN LOCALE CON MONGODB ATTIVO In DOCKER
port = "27017"


def connect_to_mongo():
    return pymongo.MongoClient("mongodb://" + username + ":" + password + "@" + db_name + ":" + port + "/")


def insert_scraping_json_list(results):
    myclient = connect_to_mongo()
    mydb = myclient["amazon-buybox"]
    mycol = mydb["scraping"]
    insert_many_result = mycol.insert_many(results)
    myclient.close()
    return insert_many_result


def insert_products_from_csv(csv_path):
    myclient = connect_to_mongo()
    mydb = myclient["amazon-buybox"]
    mycol = mydb["products"]

    # Creazione di un indice unico sul campo "id" (se non esiste già)
    mycol.create_index("id", unique=True)

    # Caricamento del CSV in un DataFrame
    df = pd.read_csv(csv_path)

    # Conversione del DataFrame in una lista di dizionari
    data = df.to_dict('records')

    # Inserimento dei dati nella collezione, con controllo dei duplicati
    for item in data:
        try:
            mycol.insert_one(item)
            logging.info(f"Inserito: {item}")
        except DuplicateKeyError:
            logging.exception(f"Duplicato trovato: {item}")

    myclient.close()

    logging.info("Data inserted successfully into the 'products' collection.")


def select_products():
    myclient = connect_to_mongo()
    mydb = myclient["amazon-buybox"]
    mycol = mydb["products"]
    product_list = list(mycol.find())
    myclient.close()
    return product_list

