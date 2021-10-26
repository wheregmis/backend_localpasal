from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
var_mongouser= os.getenv('MONGO_USERNAME')
var_mongopass= os.getenv('MONGO_PASS')
var_mongodb = os.getenv('MONGO_DATABASE')


conn = MongoClient(f"mongodb+srv://{var_mongouser}:{var_mongopass}@{var_mongodb}.nf7wz.mongodb.net/{var_mongodb}?retryWrites=true&w=majority")
mongodatabase = conn[var_mongodb]