from pymongo import MongoClient

MONGO_URI = "mongodb://mongodb:27017/"
DATABASE_NAME = "order_db"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

orders_collection = db["orders"]