import pprint

import motor.motor_asyncio
from bson import ObjectId

from src.model.RESTModel import Motorcycle


class MongoDBClient:
    def __init__(self):
        client = motor.motor_asyncio.AsyncIOMotorClient("localhost", 27017)
        self.db = client.test_database



