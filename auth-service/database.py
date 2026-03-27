from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "auth_db"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

users_collection = db["users"]
roles_collection = db["roles"]