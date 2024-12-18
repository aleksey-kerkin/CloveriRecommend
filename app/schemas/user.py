from pydantic import BaseModel


class UserBase(BaseModel):
    user_hash: str
    name: str
    recommendations: list[str]


class UserResponse(UserBase):
    class Config:
        from_attributes = True
