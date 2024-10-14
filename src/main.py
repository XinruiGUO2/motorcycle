

from fastapi import FastAPI,HTTPException
import uvicorn

from database.motor_repository import MotorRepository
from database.user_repository import UserRepository
from src.model.RESTModel import Motorcycle
from src.database.mongodb_client import MongoDBClient

app = FastAPI()

motorcycles = []

client = MongoDBClient()
user_repository = UserRepository(client.db)
motor_repository = MotorRepository(client.db)


@app.get("/")
def root():
    return {"Hello": "motorcycles"}


@app.post("/user")
async def create_user(username: str):
    user_exit = await user_repository.is_user_exist(username)
    if user_exit is False:
        inserted_id = await user_repository.do_insert_one_user(username)
        return {"inserted_user_id": str(inserted_id)}
    else:
        raise HTTPException(status_code=400, detail="User is already exited ")


@app.post("/motorcycles")
async def add_motorcycle(item: Motorcycle):
    motor_exit = await motor_repository.is_motor_exist(item.imma)
    if motor_exit is False:
        inserted_id = await motor_repository.do_insert_one_motorcycle(item)
        return {"inserted_motor_id": str(inserted_id)}
    else:
        raise HTTPException(status_code=400, detail="Motor is already exited ")


@app.get("/motorcycles")
async def list_motorcycles():
    result = await motor_repository.do_find()
    return {"motorcycles_list": str(result)}



@app.get("/motorcycles/{motorcycle_id}")
async def get_motorcycle(motorcycle_id: str) :
    document = await motor_repository.do_find_one_motorcycle(motorcycle_id)
    return {"document_find": str(document)}

@app.put("/motorcycles/{motorcycle_id}")
async def update_motorcycle(motorcycle_id: str, item: Motorcycle) :
    document = await motor_repository.do_update(motorcycle_id, item.imma)
    return {"document_update": str(document)}


@app.delete("/motorcycles/{motorcycle_id}")
async def delete_motorcycle(motorcycle_id: str) -> motorcycles:
    document = await motor_repository.do_delete_one(motorcycle_id)
    return {"document_delete": str(document)}


def start():
    """Launched with `poetry run start` at root level"""

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)