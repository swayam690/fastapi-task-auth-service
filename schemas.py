from pydantic import BaseModel,Field

class TaskInput(BaseModel):
    title:str
    description:str
    completed:bool|None = True
class TaskOutput(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
class UserInput(BaseModel):
    username:str
    password:str
class UserOutput(BaseModel):
    id:int
    username:str
