from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal
from models import UserDB
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

@app.get("/")
def home():
    return {
        "message": "AI Career Navigator Backend Running"
    }

@app.post("/register")
def register(user: User):

    db = SessionLocal()

    new_user = UserDB(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {
        "message": "User Registered Successfully"
    }

@app.get("/users")
def get_users():

    db = SessionLocal()

    all_users = db.query(UserDB).all()

    db.close()

    return all_users

@app.post("/login")
def login(data: Login):

    db = SessionLocal()

    user = db.query(UserDB).filter(
        UserDB.email == data.email,
        UserDB.password == data.password
    ).first()

    db.close()

    if user:
        return {
            "message": "Login Successful"
        }

    return {
        "message": "Invalid Credentials"
    }