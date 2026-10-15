from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.exc import IntegrityError
from schemas import TaskInput,TaskOutput,UserInput,UserOutput
from database import engine, Base,get_db
from models import Task,User
from pwdlib import PasswordHash
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_token(token: str = Depends(oauth2_scheme)):
    return token
    
pwd_hash = PasswordHash.recommended()
Base.metadata.create_all(bind=engine)
SECRET_KEY = "some-long-random-secret"
ALGORITHM = "HS256"
def create_access_token(data: dict):
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

app = FastAPI()


@app.get("/tasks/{task_id}",response_model = TaskOutput)
def get_task_id(task_id:int , db = Depends(get_db)):
    taskbyid = db.query(Task).filter(Task.id == task_id).first()
    if taskbyid is None:
        raise HTTPException(status_code = 404,detail = "id not found")
    return taskbyid




@app.get("/tasks",response_model = list[TaskOutput])
def get_tasks(db = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


@app.post("/tasks",response_model = TaskOutput)
def post_tasks(task:TaskInput,db = Depends(get_db)):
    taskobject = Task(
        title=task.title,
        description=task.description
    )
    db.add(taskobject)
    db.commit()
    db.refresh(taskobject)
    return taskobject
@app.put("/tasks/{task_id}",response_model = TaskOutput)
def update_task(task_id:int,task:TaskInput,db = Depends(get_db)):
    taskobject = db.query(Task).filter(Task.id == task_id).first()
    if taskobject is None:
        raise HTTPException(status_code = 404 ,detail = ' id not found' )
    taskobject.title = task.title
    taskobject.description = task.description
    taskobject.completed = task.completed
    db.commit()
    db.refresh(taskobject)
    return taskobject

@app.delete("/tasks/{task_id}", response_model = TaskInput)
def delete_byid(task_id:int , db = Depends(get_db)):
    taskobject = db.query(Task).filter(Task.id == task_id).first()
    if taskobject is None:
        raise HTTPException(status_code = 404 , detail= " id not found")
    db.delete(taskobject)
    db.commit()
    return taskobject

@app.post("/register" , response_model = UserOutput)
def register_user(user:UserInput , db = Depends(get_db)):
    userobject = User(
        username = user.username,
        password = pwd_hash.hash(user.password)
    )
    try:
        db.add(userobject)
        db.commit()
        db.refresh(userobject)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    return userobject
@app.post("/login")
def login_user(user:UserInput , db= Depends(get_db)):
    userobject = db.query(User).filter(User.username == user.username).first()
    if userobject is None:
        raise HTTPException(status_code = 404 , detail = " username not found")
    if not pwd_hash.verify(user.password, userobject.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )
    access_token = create_access_token({"sub":userobject.username})
    return {
        "access_token":access_token
    }
    
