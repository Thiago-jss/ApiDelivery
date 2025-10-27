from pydantic import BaseModel
from typing import Optional, List


class UserSchema(BaseModel):
    email: str
    username: str
    password: str
    active: Optional[bool]
    admin: Optional[bool] = False

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    user_id: int

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class ItemSchema(BaseModel):
    quantity: int
    flavor: str
    size: str
    unit_price: float

    class Config:
        from_attributes = True


class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    price: float
    items: List[ItemSchema]

    class Config:
        from_attributes = True
