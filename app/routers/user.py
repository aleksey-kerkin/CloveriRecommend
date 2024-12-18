from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/{user_hash}", response_model=UserResponse)
def get_user_recommendations(user_hash: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_hash == user_hash).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
