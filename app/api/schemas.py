from typing import Optional, Annotated
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr


class SignUpIn(BaseModel):
    # Схема для регистрации
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(20)]


class LoginIn(BaseModel):
    # Схема для логина
    email: EmailStr
    password: str


class UserOut(BaseModel):
    # Схема ответа сервера, когда мы возвращаем данные о пользователе
    id: int
    email: EmailStr


class TokenOut(BaseModel):
    # Схема для ответа при выдаче токена
    access_token: str
    token_type: str = "bearer"
