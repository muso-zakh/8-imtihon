from pydantic import BaseModel

class MenuBase(BaseModel):
    title: str
    url: str
    order: int = 0

class MenuCreate(MenuBase):
    pass

class MenuRead(MenuBase):
    id: int

    class Config:
        orm_mode = True
