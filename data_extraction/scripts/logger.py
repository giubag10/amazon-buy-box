import logging
import os

log_filename = os.getenv("PATH_LOGS_FILE", "../logs/amazon_data_extraction.log")
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
logging.basicConfig(filename=log_filename, format='%(asctime)s :: %(levelname)s :: %(thread)d :: \
                            %(threadName)s :: %(funcName)s :: %(lineno)d :: %(message)s'
                    , level=logging.INFO)
