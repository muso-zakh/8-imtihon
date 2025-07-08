from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class BoglanishBase(BaseModel):
    full_name_uz: Optional[str] = None
    full_name_ru: Optional[str] = None
    full_name_en: Optional[str] = None

    email: Optional[EmailStr] = None
    telefon: Optional[str] = None

    sabab_uz: Optional[str] = None
    sabab_ru: Optional[str] = None
    sabab_en: Optional[str] = None

    text_uz: Optional[str] = None
    text_ru: Optional[str] = None
    text_en: Optional[str] = None

    fayl: Optional[str] = None
    javob_berildi: Optional[bool] = False





class BoglanishCreate(BoglanishBase):
    pass


class BoglanishUpdate(BaseModel):
    full_name_uz: Optional[str] = None
    full_name_ru: Optional[str] = None
    full_name_en: Optional[str] = None

    email: Optional[EmailStr] = None
    telefon: Optional[str] = None

    sabab_uz: Optional[str] = None
    sabab_ru: Optional[str] = None
    sabab_en: Optional[str] = None

    text_uz: Optional[str] = None
    text_ru: Optional[str] = None
    text_en: Optional[str] = None

    fayl: Optional[str] = None
    javob_berildi: Optional[bool] = False



class BoglanishRead(BoglanishBase):
    id: int
    created_at: datetime
    javob_berildi: Optional[bool] = False


    class Config:
        orm_mode = True


class BoglanishLocalizedOut(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    telefon: Optional[str] = None
    sabab: Optional[str] = None
    text: Optional[str] = None
    fayl: Optional[str] = None
    created_at: datetime
    javob_berildi: Optional[bool] = False


    class Config:
        orm_mode = True
