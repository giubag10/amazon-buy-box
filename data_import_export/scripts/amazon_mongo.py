import pymongo

username = "root"
password = "amazon"
#db_name = "mongodb"  # il nome dato al container Docker di MongoDB (localhost in locale)
db_name = "localhost"  # DECOMMENTARE IN LOCALE CON MONGODB ATTIVO In DOCKER
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


def select_products():
    myclient = connect_to_mongo()
    mydb = myclient["amazon-buybox"]
    mycol = mydb["products"]
    product_list = list(mycol.find({}, {"_id": 0}))
    myclient.close()
    return product_list


def select_scraping_json_list_by_dates(start_date, end_date):
    myclient = connect_to_mongo()
    mydb = myclient["amazon-buybox"]
    mycol = mydb["scraping"]
    scraping_json_list_by_dates = list(mycol.find({"datetime_extraction": {"$gte": start_date, "$lte": end_date}},
                                                  {"_id": 0}))
    myclient.close()
    return scraping_json_list_by_dates


