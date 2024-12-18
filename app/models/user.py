from sqlalchemy import JSON, Column, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    user_hash = Column(String, primary_key=True, index=True)
    name = Column(String)
    recommendations = Column(JSON)
