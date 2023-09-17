from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config

uri = config("MONGODB_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.waterloodontwork
