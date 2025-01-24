import glob

import pandas as pd

from amazon_data_normalizer import import_json_to_dataframe, normalize_amazon_data, \
    import_document_to_dataframe
from amazon_mongo import select_scraping_json_list, select_scraping_json_list_by_dates

input_json_files_path = 'data_analysis/inputs/result*.json'


def import_input_json_files():
    file_list = glob.glob(input_json_files_path)
    data_frames = [import_json_to_dataframe(data_to_import) for data_to_import in file_list]
    return pd.concat(data_frames)


def import_input_json_files_from_dir(dir_path):
    file_list = glob.glob(dir_path + "/result*.json")
    data_frames = [import_json_to_dataframe(data_to_import) for data_to_import in file_list]
    return pd.concat(data_frames)


def import_input_json_from_db(start_date=None, end_date=None):
    if start_date is not None and end_date is not None:
        document_list = select_scraping_json_list_by_dates(start_date, end_date)
    else:
        document_list = select_scraping_json_list()
    data_frames = [import_document_to_dataframe(data_to_import) for data_to_import in document_list]
    return pd.concat(data_frames)


def import_data_to_analyze(start_date=None, end_date=None, read_from_db=False, flag_normalize=False):
    if read_from_db:
        data = import_input_json_from_db(start_date, end_date)
    else:
        data = import_input_json_files()
    if flag_normalize:
        data = normalize_amazon_data(data)
    return data
