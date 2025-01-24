import json

import pandas as pd
from sklearn.preprocessing import LabelEncoder

from logger import logging


def normalize(x):
    x_min = x.min()
    x_max = x.max()
    if x_min == x_max:
        x = 0
    else:
        x = ((x - min(x)) / (max(x) - min(x))).round(4)
    return x


def check_item_valid(item):
    return item["data"] is not None


def import_json_to_dataframe(amazon_json_data):
    # Open and read the JSON file
    with open(amazon_json_data, 'r', encoding="utf-8", newline='\n') as file:
        data = json.load(file)

    observations = []
    for item in data:
        map_item_to_dict(observations, item)

    return convert_dict_to_dataframe(observations)


def import_document_to_dataframe(amazon_document_data):
    observations = []
    map_item_to_dict(observations, amazon_document_data)
    return convert_dict_to_dataframe(observations)


def map_item_to_dict(observations, item):
    if check_item_valid(item):
        for i in range(0, len(item["data"]["other_sellers"]) + 1):
            row = {"date": item["datetime_extraction"], "name": item["name"]}
            if i == 0:
                seller = item["data"]["buybox_seller"]
                row["buybox"] = 1
            else:
                seller = item["data"]["other_sellers"][i - 1]
                row["buybox"] = 0
            row["index"] = seller["index"] + 1
            row["seller_name"] = seller["name"]
            row["price_no_shipping"] = seller["sale"]["priceNoShipping"]
            row["total_price"] = seller["sale"]["totalPrice"]
            row["price_diff_prod"] = seller["sale"]["diffPriceNoShipping"]
            row["price_diff"] = seller["sale"]["diffTotalPrice"]
            row["shipping_price"] = seller["shipping"]["price"]
            row["delivery_days"] = seller["shipping"]["days"]
            row["price_diff_ship"] = seller["shipping"]["diffPrice"]
            row["ratings_num"] = seller["ratings"]["num"]
            row["ratings_avg"] = seller["ratings"]["avg"]
            row["ratings_perc_positive"] = seller["ratings"]["perc_positive"]
            row["fba"] = seller["fba"]
            row["amazon"] = "Amazon" in seller["name"]
            row["new"] = seller["ratings"]["isNew"]
            observations.append(row)
    else:
        logging.warning("Item [" + item["datetime_extraction"] + "]-[" + item["name"] + "] is invalid")


def convert_dict_to_dataframe(data_dict):
    return pd.DataFrame(data_dict, columns=["date", "name", "buybox", "index", "seller_name", "price_no_shipping",
                                            "total_price", "price_diff_prod", "price_diff", "shipping_price",
                                            "delivery_days", "price_diff_ship", "ratings_num", "ratings_avg",
                                            "ratings_perc_positive", "fba", "amazon", "new"])


def normalize_amazon_data(df):
    df = df.fillna(0)
    # Normalizzo i dati (forse normalizzare le stringhe aiuta ulteriormente la computazione)
    le = LabelEncoder()
    df["date"] = normalize(le.fit_transform(df["date"]))  # Per una singola misurazione sarà sempre 0
    df["name"] = normalize(le.fit_transform(df["name"]))
    df["seller_name"] = normalize(le.fit_transform(df["seller_name"]))
    df["index"] = normalize(le.fit_transform(df["index"]))
    # I dati numerici (es. prezzo, numero di ratings, etc.) vanno scalati per prodotto
    columns_to_scale_by_prod = [
        "price_no_shipping", "shipping_price", "total_price", "delivery_days",
        "ratings_num", "price_diff_prod", "price_diff", "price_diff_ship"]
    df[columns_to_scale_by_prod] = df.groupby(["name", "date"])[columns_to_scale_by_prod].transform(
        lambda x: normalize(le.fit_transform(x)))
    # Valori già scalati per l'intero Dataset, solo da normalizzare
    df["ratings_avg"] = normalize(le.fit_transform(df["ratings_avg"]))
    df["ratings_perc_positive"] = normalize(le.fit_transform(df["ratings_perc_positive"]))
    df["buybox"] = le.fit_transform(df["buybox"])
    df["fba"] = le.fit_transform(df["fba"])
    df["amazon"] = le.fit_transform(df["amazon"])

    log_statistics(df)

    return df


def get_bb_rows(df):
    return df[df['buybox'] == 1]


def get_nbb_rows(df):
    return df[df['buybox'] == 0]


def get_fba_rows(df):
    return df[df['fba'] == 1]


def get_nfba_rows(df):
    return df[df['fba'] == 0]


def get_amazon_rows(df):
    return df[df['amazon'] == 1]


def get_namazon_rows(df):
    return df[df['amazon'] == 0]


def calculate_statistics(df):
    buy_box = get_bb_rows(df)
    fba = get_fba_rows(buy_box)
    fba_winner = len(fba) / len(buy_box)
    amazon_winner = len(get_amazon_rows(buy_box)) / len(buy_box)
    fba_winner_not_amazon = len(get_namazon_rows(fba)) / len(buy_box)
    fbm_winner = len(get_nfba_rows(buy_box)) / len(buy_box)
    return fba_winner, amazon_winner, fba_winner_not_amazon, fbm_winner


def calculate_statistics_on_df(df):
    fba_winner, amazon_winner, fba_winner_not_amazon, fbm_winner = calculate_statistics(df)
    statistics_dict = {
        "name": ["Amazon seller", "FBA third party seller", "FBM third party seller"],
        "perc": [round(amazon_winner * 100, 1), round(fba_winner_not_amazon * 100, 1), round(fbm_winner * 100, 1)]
    }
    return pd.DataFrame(statistics_dict)


def log_statistics(df):
    fba_winner, amazon_winner, fba_winner_not_amazon, fbm_winner = calculate_statistics(df)
    logging.info('PERCENTUALE FBA_WINNER : ' + str(fba_winner))
    logging.info('PERCENTUALE AMAZON_WINNER : ' + str(amazon_winner))
    logging.info('PERCENTUALE FBA_WINNER CHE NON E\' AMAZON: ' + str(fba_winner_not_amazon))
    logging.info('PERCENTUALE FBM WINNER: ' + str(fbm_winner))


def ml_analysis_output_to_df(ml_analysis_output):
    df = pd.DataFrame(columns=["alg_name", "accuracy", "feature", "importance"])
    for item in ml_analysis_output:
        df_importance = item["perm_importance"].reset_index().rename(columns={"index": "feature", 0: "importance"})
        df_importance["alg_name"] = item["alg_name"]
        df_importance["accuracy"] = item["accuracy"]
        df = pd.concat([df, df_importance])

    return df

