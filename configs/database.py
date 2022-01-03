import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
var_mongo_user= os.getenv('MONGO_USERNAME')
var_mongo_pass= os.getenv('MONGO_PASS')
var_mongodb = os.getenv('MONGO_DATABASE')


conn = MongoClient(f"mongodb+srv://{var_mongo_user}:{var_mongo_pass}@{var_mongodb}.nf7wz.mongodb.net/{var_mongodb}?retryWrites=true&w=majority")
mongodatabase = conn[var_mongodb]