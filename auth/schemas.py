from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str | None = None
    email: EmailStr
    password: str

from pydantic import BaseModel, EmailStr

class UserRead(BaseModel):
    id: int
    username: str | None = None
    email: EmailStr
    is_superuser: bool
    admin: bool
    is_active: bool

    class Config:
        orm_mode = True

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class LoginInput(BaseModel):
    email: EmailStr
    password: str

    


class LoginInput(BaseModel):
    email: EmailStr
    password: str
