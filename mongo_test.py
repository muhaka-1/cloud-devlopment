from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["shop"]

print("Connected!")

collections = db.list_collection_names()

print(collections)

