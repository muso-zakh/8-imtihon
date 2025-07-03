from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str | None = None
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_superuser: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
