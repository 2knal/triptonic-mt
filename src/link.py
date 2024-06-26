import pymongo
from src.utils import load_secrets
import random
import string

class MagicLink(object):
    mongo_connection_string = load_secrets()['MONGO_CONNECTION_STRING']
    website_domain = load_secrets()['WEBSITE_DOMAIN']
    mongo_client = pymongo.MongoClient(mongo_connection_string)
    mongo_db = mongo_client.get_database('TripTonicDump')
    mongo_collection = pymongo.collection.Collection(mongo_db, 'MagicLink')

    @staticmethod
    def generate_link():
        random_str = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=5))
        while MagicLink.mongo_collection.find_one({"link": random_str}):
            random_str = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=5))
        return random_str

    @staticmethod
    def save_update_trip(link, name, params, places):
        if MagicLink.mongo_collection.find_one({"link": link}):
            MagicLink.mongo_collection.update_one({"link": link}, {"$set": {"places": places, "name": name, "params": params}})
        else:
            MagicLink.mongo_collection.insert_one({"link": link, "places": places, "name": name, "params": params})

    @staticmethod
    def get_trip(link):
        res = MagicLink.mongo_collection.find_one({"link": MagicLink.website_domain + link})
        return {
            "places": res['places'],
            "params": res['params'],
            "name": res['name']
        }
