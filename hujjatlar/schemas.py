from pydantic import BaseModel
from typing import Optional
from datetime import date


class HujjatBase(BaseModel):
    guruhi: str

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    shifr: str

    xujjat_nomi_uz: str
    xujjat_nomi_ru: str
    xujjat_nomi_en: str

    xavola: str  # PDF fayl manzili


class HujjatCreate(HujjatBase):
    pass


class HujjatUpdate(BaseModel):
    guruhi: Optional[str] = None


    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    shifr: Optional[str] = None

    xujjat_nomi_uz: Optional[str] = None
    xujjat_nomi_ru: Optional[str] = None
    xujjat_nomi_en: Optional[str] = None

    xavola: Optional[str] = None


class HujjatlarLocalizedOut(BaseModel):
    id: int
    guruhi: str
    desc: Optional[str]
    shifr: str
    xujjat_nomi: str
    xavola: str  # PDF fayl manzili


class HujjatRead(HujjatBase):
    id: int

    class Config:
        orm_mode = True




"""standardlar"""



class StandartBase(BaseModel):
    title_uz: str
    title_ru: str
    title_en: str

    created_at: date

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    konsultatsiya_uz: Optional[str] = None
    konsultatsiya_ru: Optional[str] = None
    konsultatsiya_en: Optional[str] = None

    rasm: Optional[str] = None  # Fayl yo‘li yoki URL


class StandartCreate(StandartBase):
    pass


class StandartUpdate(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None

    created_at: Optional[date] = None

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    konsultatsiya_uz: Optional[str] = None
    konsultatsiya_ru: Optional[str] = None
    konsultatsiya_en: Optional[str] = None

    rasm: Optional[str] = None


class StandartRead(StandartBase):
    id: int

    class Config:
        orm_mode = True



class StandartLocalizedOut(BaseModel):
    id: int
    title: str
    created_at: date
    desc: Optional[str] = None
    konsultatsiya: Optional[str] = None
    rasm: Optional[str] = None

    class Config:
        orm_mode = True



"""Qurilish Reglamentlar"""

from pydantic import BaseModel
from typing import Optional


class QurilishReglamentBase(BaseModel):
    belgilanishi_uz: str
    belgilanishi_ru: str
    belgilanishi_en: str

    title_uz: str
    title_ru: str
    title_en: str

    hujjat: str  # PDF fayl manzili


class QurilishReglamentCreate(QurilishReglamentBase):
    pass


class QurilishReglamentUpdate(BaseModel):
    belgilanishi_uz: Optional[str] = None
    belgilanishi_ru: Optional[str] = None
    belgilanishi_en: Optional[str] = None

    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None

    hujjat: Optional[str] = None


class QurilishReglamentRead(QurilishReglamentBase):
    id: int

    class Config:
        orm_mode = True


class QurilishReglamentLocalizedOut(BaseModel):
    id: int
    belgilanishi: str
    title: str
    hujjat: str

    class Config:
        orm_mode = True



"""Smeta Resurslar Nomi"""

class SmetaResursBase(BaseModel):
    new_shnq_raqam: str

    new_shnq_nomi_uz: str
    new_shnq_nomi_ru: str
    new_shnq_nomi_en: str

    shnq_raqam: str

    shnq_nomi_uz: str
    shnq_nomi_ru: str
    shnq_nomi_en: str

    fayl: str  # Fayl yo‘li (masalan: uploads/fayl.pdf)


class SmetaResursCreate(SmetaResursBase):
    pass


class SmetaResursUpdate(BaseModel):
    new_shnq_raqam: Optional[str] = None

    new_shnq_nomi_uz: Optional[str] = None
    new_shnq_nomi_ru: Optional[str] = None
    new_shnq_nomi_en: Optional[str] = None

    shnq_raqam: Optional[str] = None

    shnq_nomi_uz: Optional[str] = None
    shnq_nomi_ru: Optional[str] = None
    shnq_nomi_en: Optional[str] = None

    fayl: Optional[str] = None


class SmetaResursRead(SmetaResursBase):
    id: int

    class Config:
        orm_mode = True


class SmetaResursLocalizedOut(BaseModel):
    id: int
    new_shnq_raqam: str
    new_shnq_nomi: str
    shnq_raqam: str
    shnq_nomi: str
    fayl: str

    class Config:
        orm_mode = True




"""Malumotnoma"""

class MalumotnomaBase(BaseModel):
    nomi_uz: str
    nomi_ru: str
    nomi_en: str
    hujjat: str  # Fayl yo‘li (masalan: uploads/hujjat.pdf)


class MalumotnomaCreate(MalumotnomaBase):
    pass


class MalumotnomaUpdate(BaseModel):
    nomi_uz: Optional[str] = None
    nomi_ru: Optional[str] = None
    nomi_en: Optional[str] = None
    hujjat: Optional[str] = None


class MalumotnomaRead(MalumotnomaBase):
    id: int

    class Config:
        orm_mode = True


class MalumotnomaLocalizedOut(BaseModel):
    id: int
    nomi: str
    hujjat: str

    class Config:
        orm_mode = True
