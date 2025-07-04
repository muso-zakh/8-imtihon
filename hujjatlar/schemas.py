from pydantic import BaseModel
from typing import Optional
from datetime import date


class HujjatBase(BaseModel):
    guruhi: str
    desc: str | None = None
    shifr: str
    xujjat_nomi: str
    xavola: str  # PDF fayl manzili (masalan: uploads/pdf/example.pdf)


class HujjatCreate(HujjatBase):
    pass


class HujjatUpdate(BaseModel):
    guruhi: str | None = None
    desc: str | None = None
    shifr: str | None = None
    xujjat_nomi: str | None = None
    xavola: str | None = None


class HujjatRead(HujjatBase):
    id: int

    class Config:
        orm_mode = True



"""standardlar"""



class StandartBase(BaseModel):
    title: str
    created_at: date
    desc: Optional[str] = None
    konsultatsiya: Optional[str] = None
    rasm: Optional[str] = None  # Fayl yo‘li yoki URL


class StandartCreate(StandartBase):
    pass  # Fayl `UploadFile` orqali routerda olinadi, schema orqali emas


class StandartUpdate(BaseModel):
    title: Optional[str] = None
    created_at: Optional[date] = None
    desc: Optional[str] = None
    konsultatsiya: Optional[str] = None
    rasm: Optional[str] = None


class StandartRead(StandartBase):
    id: int

    class Config:
        orm_mode = True