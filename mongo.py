import pandas as pd
from pymongo import MongoClient
import json


def mongoimport(csv_path, db_name, coll_name, db_url='localhost', db_port=27017):
    """ Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection
    """
    client = MongoClient(db_url, db_port)
    db = client[db_name]
    coll = db[coll_name]
    data = pd.read_csv(csv_path, encoding="utf-8")
    payload = json.loads(data.to_json(orient='records'))
    coll.delete_many({})
    coll.insert_many(payload)
    for x in coll.find():
        print(x)


mongoimport("./csv/colors.csv",
            "coloravg", "color")
mongoimport("./csv/styles.csv",
            "coloravg", "styles")
mongoimport("./csv/colors_recommend_styles.csv",
            "coloravg", "colors_recommend_styles")
