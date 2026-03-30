from pymongo import MongoClient

MONGO_URI = "mongodb://mongodb:27017/"
DATABASE_NAME = "product_db"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

products_collection = db["products"]