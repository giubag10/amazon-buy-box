# Filtro per un nuovo venditore presente come vincitore della BB (filtra le osservazioni)
def filter_new_bb_sellers(df):
    df_with_new_bb_seller = df[(df["index"] == 1) & (df["new"] == True)]
    obs_to_filter = list(zip(df_with_new_bb_seller["name"], df_with_new_bb_seller["date"]))
    return df[~df[["name", "date"]].apply(tuple, axis=1).isin(obs_to_filter)]


# Filtro per un nuovo venditore presente come venditore non vincitore della BB
def filter_new_nbb_sellers(df):
    return df[~((df["index"] != 1) & (df["new"] == True))]


# Filtro per amazon presente come vincitore della BuyBox (filtra le osservazioni)
def filter_amazon_bb_seller(df):
    df_with_amazon_bb_seller = df[(df["index"] == 1) & (df["amazon"] == True)]
    obs_to_filter = list(zip(df_with_amazon_bb_seller["name"], df_with_amazon_bb_seller["date"]))
    return df[~df[["name", "date"]].apply(tuple, axis=1).isin(obs_to_filter)]


# Filtro per amazon presente come venditore non vincitore della BB
def filter_amazon_nbb_seller(df):
    return df[~((df["index"] != 1) & (df["amazon"] == True))]


# Filtro per data inizio e fine
def filter_by_dates(df, start_date, end_date):
    return df[df["date"].between(start_date, end_date)]


# Filtro per numero minimo di venditori per osservazione
def filter_by_seller_count(df, seller_count):
    return df.groupby(["name", "date"]).filter(lambda x: max(x["index"]) >= seller_count + 1)


# Filtro per numero di venditori non vincitori di BB
def filter_by_nbb_seller_count(df, nbb_seller_count):
    return df[df["index"] <= nbb_seller_count + 1]


def apply_filters(df, start_date, end_date, seller_count, nbb_seller_count, radio_amazon_bb, radio_amazon_nbb,
                  radio_new_bb, radio_new_nbb):
    filtered_data = filter_by_dates(df, start_date, end_date)
    filtered_data = apply_filters_no_dates(filtered_data, seller_count, nbb_seller_count, radio_amazon_bb,
                                           radio_amazon_nbb, radio_new_bb, radio_new_nbb)
    return filtered_data


def apply_filters_no_dates(filtered_data, seller_count, nbb_seller_count, radio_amazon_bb, radio_amazon_nbb,
                           radio_new_bb, radio_new_nbb):
    filtered_data = filter_by_seller_count(filtered_data, seller_count)
    filtered_data = filter_by_nbb_seller_count(filtered_data, nbb_seller_count)
    if radio_amazon_bb:
        filtered_data = filter_amazon_bb_seller(filtered_data)
    if radio_amazon_nbb:
        filtered_data = filter_amazon_nbb_seller(filtered_data)
    if radio_new_bb:
        filtered_data = filter_new_bb_sellers(filtered_data)
    if radio_new_nbb:
        filtered_data = filter_new_nbb_sellers(filtered_data)
    return filtered_data

