from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class CareerDB(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    skills = Column(String)
    description = Column(String)

class SkillDB(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String)
    category = Column(String)

class UserSkillDB(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    skill_name = Column(String)

