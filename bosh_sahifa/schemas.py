from pydantic import BaseModel
from typing import Optional


class BoshSahifaBase(BaseModel):
    tavsif_uz: str
    tavsif_ru: str
    tavsif_en: str
    shnq_uz: str
    shnq_ru: str
    shnq_en: str
    standartlar_uz: str
    standartlar_ru: str
    standartlar_en: str
    tashkilot_nomi_uz: str
    tashkilot_nomi_ru: str
    tashkilot_nomi_en: str

    rasm: str  # Fayl yo‘li yoki URL


class BoshSahifaCreate(BoshSahifaBase):
    pass


class BoshSahifaRead(BoshSahifaBase):
    id: int

    class Config:
        orm_mode = True


class TranslatedBoshSahifaRead(BaseModel):
    id: int
    tavsif: str
    SHNQ: str
    standartlar: str
    tashkilot_nomi: str
    rasm: str
