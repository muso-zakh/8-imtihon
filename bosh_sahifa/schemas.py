from pydantic import BaseModel

class BoshSahifaBase(BaseModel):
    tavsif: str
    SHNQ: str
    standartlar: str
    tashkilot_nomi: str
    rasm: str

class BoshSahifaCreate(BoshSahifaBase):
    pass

class BoshSahifaRead(BoshSahifaBase):
    id: int

    class Config:
        orm_mode = True
