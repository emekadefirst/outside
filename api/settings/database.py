import os
from dotenv import load_dotenv
from pymongo import MongoClient



load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)

db = client["OutsideCluster"]
