from pymongo import MongoClient

cluster = 'mongodb://localhost:27017/elibraryAPI'
client = MongoClient(cluster)

db = client.elibraryAPI
