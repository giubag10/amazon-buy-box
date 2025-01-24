import json

from amazon_mongo import select_scraping_json_list_by_dates
from logger import logging

start_date = "2024-09-09"
end_date = "2025-01-01"
file_json = "scraping_data_export_"+start_date+"_"+end_date+".json"


# Esporta in JSON i dati da MongoDB, che potranno essere importati con amazon_data_importer.py
def export_scraping_data_in_json():
    scraping_json_list = select_scraping_json_list_by_dates(start_date, end_date)
    logging.info(str(len(scraping_json_list)) + "records scraped")

    with open(file_json, "w") as outfile:
        json.dump(scraping_json_list, outfile)

    logging.info(f"{file_json} exported")


if __name__ == "__main__":
    export_scraping_data_in_json()
    print(f"Dati inseriti correttamente dal file {file_json}")
