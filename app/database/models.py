# app/database/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    plants = relationship("UserPlant", back_populates="user")


class Plant(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, index=True)
    scientific_name = Column(String, unique=True, index=True, nullable=False)
    family = Column(String, index=True, nullable=False)
    is_edible = Column(Boolean, index=True, nullable=False)
    # Optional fields (can be null)
    edible_parts = Column(String, nullable=True)  # Stored as a comma-separated string.
    safety = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("UserPlant", back_populates="plant")


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    content = Column(String, unique=True, index=True, nullable=False)


class UserPlant(Base):
    __tablename__ = "user_plants"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    image = Column(String, nullable=True)  # Ignored for now (set to null)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String, nullable=True)

    user = relationship("User", back_populates="plants")
    plant = relationship("Plant", back_populates="users")
