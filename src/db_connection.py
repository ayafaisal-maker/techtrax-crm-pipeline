import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def get_client():
    uri = os.getenv("MONGO_PROD_URI")
    return MongoClient(uri)