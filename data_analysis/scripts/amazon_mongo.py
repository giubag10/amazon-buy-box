import pymongo

username = "root"
password = "amazon"
db_name = "mongodb"  # il nome dato al container Docker di MongoDB (localhost in locale)
# db_name = "localhost"  # DECOMMENTARE IN LOCALE CON MONGODB ATTIVO In DOCKER
port = "27017"


def connect_to_mongo():
    return pymongo.MongoClient("mongodb://" + username + ":" + password + "@" + db_name + ":" + port + "/")


def select_scraping_json_list():
    myclient = connect_to_mongo()
    mydb = myclient["amazon-buybox"]
    mycol = mydb["scraping"]
    scraping_json_list = list(mycol.find({"data": {"$ne": "null"}}))
    myclient.close()
    return scraping_json_list


def select_scraping_json_list_by_dates(start_date, end_date):
    myclient = connect_to_mongo()
    mydb = myclient["amazon-buybox"]
    mycol = mydb["scraping"]
    scraping_json_list_by_dates = list(mycol.find({"data": {"$ne": "null"}, "datetime_extraction": {"$gte": start_date, "$lte": end_date}}))
    myclient.close()
    return scraping_json_list_by_dates


def select_max_and_min_dates():
    myclient = connect_to_mongo()
    mydb = myclient["amazon-buybox"]
    mycol = mydb["scraping"]
    min_date = mycol.find_one(sort=[("datetime_extraction", pymongo.ASCENDING)])["datetime_extraction"]
    max_date = mycol.find_one(sort=[("datetime_extraction", pymongo.DESCENDING)])["datetime_extraction"]
    myclient.close()
    return min_date, max_date

