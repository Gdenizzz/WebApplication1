from pymongo import MongoClient

MONGO_URI = "mongodb://mongodb:27017/"
DATABASE_NAME = "dispatcher_db"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

logs_collection = db["logs"]