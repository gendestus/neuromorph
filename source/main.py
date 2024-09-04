import datetime

from fastapi import FastAPI

from pymongo import MongoClient

from systems.observer import Observation, observe
from utils import DB_NAME, OUTPUT_COLLECTION

app = FastAPI()

@app.post("/observe")
def post_observation(observation: Observation):
    return observe(observation)

@app.get("/test/input")
def get_test_input():
    client = MongoClient("mongodb://localhost:27017/")
    db = client[DB_NAME]
    collection = db[OUTPUT_COLLECTION]
    test_doc = {
        "timestamp": datetime.datetime.now().isoformat(),
        "source": "test",
        "observation": "this is a test"
    }
    collection.insert_one(test_doc)
    return test_doc

@app.get("/test/output")
def get_test_output():
    client = MongoClient("mongodb://localhost:27017/")
    db = client[DB_NAME]
    collection = db[OUTPUT_COLLECTION]
    return list(collection.find())