from sqlalchemy import Column, Integer, String, Boolean, ColumnElement
from app.database.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class Plant(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, index=True)
    scientific_name = Column(String, unique=True, index=True, nullable=False)
    family = Column(String, index=True, nullable=False)
    is_edible = Column(Boolean, index=True, nullable=False)
