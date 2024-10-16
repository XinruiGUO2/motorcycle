import pprint

from bson import ObjectId
from motor.core import AgnosticDatabase


class UserRepository:
    def __init__(self, db: AgnosticDatabase):
        self.collection_user = db.user_collection

    async def do_insert_one_user(self, username: str):
        document = {"username": username}
        result = await self.collection_user.insert_one(document)
        print("result %s" % repr(result.inserted_id))
        return result.inserted_id

    async def do_find_one_user(self, _id: str):
        document = await self.collection_user.find_one({"_id": ObjectId(_id)})
        pprint.pprint(document)
        return document



    async def is_user_exist(self, username: str) -> bool:
        c = self.collection_user
        n = await c.count_documents({"username": {"$eq": username}})
        return n > 0