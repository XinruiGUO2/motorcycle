import pprint

from bson import ObjectId
from motor.core import AgnosticDatabase

from src.model.RESTModel import Motorcycle


class MotorRepository:
    def __init__(self, db: AgnosticDatabase):
        self.collection_motor = db.motor_collection

    async def do_insert_one_motorcycle(self, item: Motorcycle):
        document = {"imma": item.imma, "userid": item.userId}

        result = await self.collection_motor.insert_one(document)
        print("result %s" % repr(result.inserted_id))
        return result.inserted_id


    async def do_find_one_motorcycle(self, _id: str) :
        document = await self.collection_motor.find_one({"_id": ObjectId(_id)})
        pprint.pprint(document)
        return document


    async def do_find(self):
        c = self.collection_motor
        l = []
        async for document in c.find({}):
            l.append(document)
            pprint.pprint(document)
        return l


    async def find_motors_by_userid(self, userid: str):
        c = self.collection_motor
        l = []
        async for document in c.find({"userid": {"$eq": ObjectId(userid)}}):
            l.append(document)
            pprint.pprint(document)
        return l


    async def is_motor_exist(self, imma: str) -> bool:
        c = self.collection_motor

        n = await c.count_documents({"imma": {"$eq": imma}})
        return n > 0


    async def do_update(self, _id: str, imma: str):
        coll = self.collection_motor
        result = await coll.update_one({"_id": ObjectId(_id)}, {"$set": {"imma": imma}})
        print("updated %s document" % result.modified_count)
        new_document = await coll.find_one({"_id": ObjectId(_id)})
        print("document is now %s" % pprint.pformat(new_document))
        return new_document


    async def do_delete_one(self, _id: str):
        coll = self.collection_motor
        n = await coll.count_documents({})
        print("%s documents before calling delete_one()" % n)
        result = await coll.delete_one({"_id": ObjectId(_id)})
        print("%s documents after" % (await coll.count_documents({})))
        return result