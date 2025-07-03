from pydantic import BaseModel

class InstitutBase(BaseModel):
    malumot: str
    text: str

class InstitutCreate(InstitutBase):
    pass

class InstitutRead(InstitutBase):
    id: int
    guvonoma: str

    class Config:
        orm_mode = True