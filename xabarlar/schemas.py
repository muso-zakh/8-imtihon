from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


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




"""Yangiliklar"""

class YangilikBase(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    rasm: Optional[str] = None  # Rasm fayl yo‘li yoki URL


class YangilikCreate(YangilikBase):
    pass


class YangilikUpdate(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    rasm: Optional[str] = None


class YangilikRead(YangilikBase):
    id: int
    created_at: datetime
    views_count: int

    class Config:
        orm_mode = True


class YangilikLocalizedOut(BaseModel):
    id: int
    title: str
    desc: Optional[str] = None
    rasm: Optional[str] = None
    created_at: datetime
    views_count: int

    class Config:
        orm_mode = True




"""Uchrashuvlar"""

class UchrashuvBase(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    place_uz: Optional[str] = None
    place_ru: Optional[str] = None
    place_en: Optional[str] = None

    rasm: Optional[str] = None  # Rasm fayl yo‘li yoki URL
    date: Optional[datetime] = None


class UchrashuvCreate(UchrashuvBase):
    pass


class UchrashuvUpdate(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    place_uz: Optional[str] = None
    place_ru: Optional[str] = None
    place_en: Optional[str] = None

    rasm: Optional[str] = None
    date: Optional[datetime] = None


class UchrashuvRead(UchrashuvBase):
    id: int

    class Config:
        orm_mode = True


class UchrashuvLocalizedOut(BaseModel):
    id: int
    title: str
    desc: Optional[str] = None
    place: Optional[str] = None
    rasm: Optional[str] = None
    date: datetime

    class Config:
        orm_mode = True




"""Ommaviy Tadbirlar"""

class TadbirBase(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    place_uz: Optional[str] = None
    place_ru: Optional[str] = None
    place_en: Optional[str] = None

    rasm: Optional[str] = None  # Fayl yo‘li
    date: Optional[datetime] = None


class TadbirCreate(TadbirBase):
    pass


class TadbirUpdate(BaseModel):
    title_uz: Optional[str] = None
    title_ru: Optional[str] = None
    title_en: Optional[str] = None

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    place_uz: Optional[str] = None
    place_ru: Optional[str] = None
    place_en: Optional[str] = None

    rasm: Optional[str] = None
    date: Optional[datetime] = None


class TadbirRead(TadbirBase):
    id: int

    class Config:
        orm_mode = True


class TadbirLocalizedOut(BaseModel):
    id: int
    title: str
    desc: Optional[str] = None
    place: Optional[str] = None
    rasm: Optional[str] = None
    date: datetime

    class Config:
        orm_mode = True




"""Xalqaro Hamkorlik"""

class XalqaroHamkorlikBase(BaseModel):
    hamkorliklar_uz: Optional[str] = None
    hamkorliklar_ru: Optional[str] = None
    hamkorliklar_en: Optional[str] = None

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    rasm: Optional[str] = None  # Fayl yo‘li yoki URL
    date: Optional[datetime] = None


class XalqaroHamkorlikCreate(XalqaroHamkorlikBase):
    pass


class XalqaroHamkorlikUpdate(BaseModel):
    hamkorliklar_uz: Optional[str] = None
    hamkorliklar_ru: Optional[str] = None
    hamkorliklar_en: Optional[str] = None

    desc_uz: Optional[str] = None
    desc_ru: Optional[str] = None
    desc_en: Optional[str] = None

    rasm: Optional[str] = None
    date: Optional[datetime] = None


class XalqaroHamkorlikRead(XalqaroHamkorlikBase):
    id: int

    class Config:
        orm_mode = True


class XalqaroHamkorlikLocalizedOut(BaseModel):
    id: int
    hamkorliklar: str
    desc: Optional[str] = None
    rasm: Optional[str] = None
    date: datetime

    class Config:
        orm_mode = True




"""Seminar Korgazmalar"""

class SeminarKorgazmaBase(BaseModel):
    nomi_uz: Optional[str] = None
    nomi_ru: Optional[str] = None
    nomi_en: Optional[str] = None

    tavsif_uz: Optional[str] = None
    tavsif_ru: Optional[str] = None
    tavsif_en: Optional[str] = None

    place_uz: Optional[str] = None
    place_ru: Optional[str] = None
    place_en: Optional[str] = None

    tashkilotchi_uz: Optional[str] = None
    tashkilotchi_ru: Optional[str] = None
    tashkilotchi_en: Optional[str] = None

    aloqa: Optional[str] = None  # telefon yoki email
    banner: Optional[str] = None  # rasm yo‘li yoki URL
    datee: Optional[date] = None  # foydalanuvchi '2022-02-02' formatda kiritadi


class SeminarKorgazmaCreate(SeminarKorgazmaBase):
    pass


class SeminarKorgazmaUpdate(BaseModel):
    nomi_uz: Optional[str] = None
    nomi_ru: Optional[str] = None
    nomi_en: Optional[str] = None

    tavsif_uz: Optional[str] = None
    tavsif_ru: Optional[str] = None
    tavsif_en: Optional[str] = None

    place_uz: Optional[str] = None
    place_ru: Optional[str] = None
    place_en: Optional[str] = None

    tashkilotchi_uz: Optional[str] = None
    tashkilotchi_ru: Optional[str] = None
    tashkilotchi_en: Optional[str] = None

    aloqa: Optional[str] = None
    banner: Optional[str] = None
    datee: Optional[date] = None


class SeminarKorgazmaRead(SeminarKorgazmaBase):
    id: int

    class Config:
        orm_mode = True


class SeminarKorgazmaLocalizedOut(BaseModel):
    id: int
    nomi: str
    tavsif: Optional[str] = None
    place: Optional[str] = None
    tashkilotchi: Optional[str] = None
    aloqa: Optional[str] = None
    banner: Optional[str] = None
    datee: date

    class Config:
        orm_mode = True





"""Korrupsiya"""

class KorrupsiyaBase(BaseModel):
    text_uz: Optional[str] = None
    text_ru: Optional[str] = None
    text_en: Optional[str] = None

    qonun_uz: Optional[str] = None
    qonun_ru: Optional[str] = None
    qonun_en: Optional[str] = None

    aloqa: Optional[str] = None
    rasm: Optional[str] = None


class KorrupsiyaCreate(KorrupsiyaBase):
    pass


class KorrupsiyaUpdate(BaseModel):
    text_uz: Optional[str] = None
    text_ru: Optional[str] = None
    text_en: Optional[str] = None

    qonun_uz: Optional[str] = None
    qonun_ru: Optional[str] = None
    qonun_en: Optional[str] = None

    aloqa: Optional[str] = None
    rasm: Optional[str] = None


class KorrupsiyaRead(KorrupsiyaBase):
    id: int

    class Config:
        orm_mode = True


class KorrupsiyaLocalizedOut(BaseModel):
    id: int
    text: Optional[str] = None
    qonun: Optional[str] = None
    aloqa: Optional[str] = None
    rasm: Optional[str] = None

    class Config:
        orm_mode = True
