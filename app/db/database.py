from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./user_recommendations.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
