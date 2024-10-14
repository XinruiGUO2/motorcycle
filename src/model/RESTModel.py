from pydantic import BaseModel


class Motorcycle(BaseModel):
    userId: str
    imma: str

class User(BaseModel):
    username: str

