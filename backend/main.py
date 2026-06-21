from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal
from models import UserDB, CareerDB
from database import engine
from models import Base
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from fastapi import Header
from jose import JWTError
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

Base.metadata.create_all(bind=engine)

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class Career(BaseModel):
    title: str
    skills: str
    description: str

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None

@app.get("/")
def home():
    return {
        "message": "AI Career Navigator Backend Running"
    }

@app.post("/register")
def register(user: User):

    db = SessionLocal()

    existing_user = db.query(UserDB).filter(
        UserDB.email == user.email
    ).first()

    if existing_user:
        db.close()
        return {
            "message": "Email already registered"
        }

    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = UserDB(
        name=user.name,
        email=user.email,
        password=hashed_password
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
        UserDB.email == data.email
    ).first()

    db.close()

    if user and bcrypt.checkpw(
        data.password.encode("utf-8"),
        user.password.encode("utf-8")
    ):

        access_token = create_access_token(
            data={"sub": user.email}
        )

        return {
            "message": "Login Successful",
            "access_token": access_token
        }

    return {
        "message": "Invalid Credentials"
    }

@app.get("/profile")
def profile(token: str):

    payload = verify_token(token)

    if not payload:
        return {
            "message": "Invalid Token"
        }

    email = payload["sub"]

    db = SessionLocal()

    user = db.query(UserDB).filter(
        UserDB.email == email
    ).first()

    db.close()

    if not user:
        return {
            "message": "User Not Found"
        }

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

@app.post("/career")
def add_career(career: Career):

    db = SessionLocal()

    new_career = CareerDB(
        title=career.title,
        skills=career.skills,
        description=career.description
    )

    db.add(new_career)
    db.commit()

    db.close()

    return {
        "message": "Career Added Successfully"
    }

@app.get("/careers")
def get_careers():

    db = SessionLocal()

    careers = db.query(CareerDB).all()

    db.close()

    return careers

@app.get("/career/{career_id}")
def get_career(career_id: int):

    db = SessionLocal()

    career = db.query(CareerDB).filter(
        CareerDB.id == career_id
    ).first()

    db.close()

    if not career:
        return {
            "message": "Career Not Found"
        }

    return career
