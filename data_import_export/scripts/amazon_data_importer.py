import json
import sys

from amazon_mongo import insert_scraping_json_list
from logger import logging


# Importa in MongoDB i dati esportati con amazon_data_exporter.py
def import_scraping_data_from_json(file_json_input):
    with open(file_json_input, "r") as json_input:
        data = json.load(json_input)

    insert_scraping_json_list(data)
    logging.info("Successfully imported scraping data")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Utilizzo: python .\\data_import_export\\scripts\\amazon_data_importer.py nome_file.json")
        sys.exit(1)

    file_json = sys.argv[1]
    import_scraping_data_from_json(file_json)
    print(f"Dati inseriti correttamente dal file {file_json}")

