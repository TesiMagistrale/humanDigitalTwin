from datetime import datetime
import json
from domain.ports.DbPort import DbPort
from pymongo import MongoClient

class MongoDbAdapter(DbPort):
    
    def __init__(self, database_uri, database_name):
        self.client = MongoClient(database_uri)
        self.db = self.client[database_name]
        
    def insert(self, id, collection_name, data):
        data["id_person"] = id
        filter = {"id_person": id}
        self.db[collection_name].update_one(filter, {"$setOnInsert": data}, upsert=True)

        
    def new_person_info(self, id, collection_name, info, value):
        self.db[collection_name].update_one(
            {"id_person": id},
            {"$set": {info: value}}
        )
        
    def update_general_data(self, id, collection_name, key, value):
        self.db[collection_name].update_one(
            {"id_person": id},
            [{'$set': {key: value}}]
            )
    
    def new_chatacteristic_value(self, id, collection_name, characteristic, value):
        date = value["date"]
        self.db[collection_name].update_one(
            {"id_person": id},
            [{'$set': {characteristic: {str(date): value["value"]}}}]
            )
        

    def get_all_chatacteristic_values(self, id, collection_name, characteristic):
        person_document = self.db[collection_name].find_one({"id_person": id})

        # Get all characteristic values from the person's document
        return person_document.get(characteristic, {})

    def get_characteristic_range_values(self, id, collection_name, characteristic, start, end):
        person_document = self.db[collection_name].find_one({"id_person": id})
        
        # Get all "characteristic_values" values from the person's document within the date range
        characteristic_values = person_document.get(characteristic, {})
        filtered_km_values = {date: value for date, value in characteristic_values.items()
                            if start <= int(date) <= end}
        return filtered_km_values
    