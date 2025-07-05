from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ElonBase(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    rasm: Optional[str] = None  # Rasm fayl yo‘li yoki URL


class ElonCreate(ElonBase):
    pass


class ElonUpdate(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    rasm: Optional[str] = None


class ElonRead(ElonBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ElonLocalizedOut(BaseModel):
    id: int
    title: str
    desc: Optional[str] = None
    rasm: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
