from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# ==== Institut ====

class InstitutBase(BaseModel):
    malumot_uz: str
    malumot_ru: str
    malumot_en: str

    text_uz: str
    text_ru: str
    text_en: str

class InstitutCreate(InstitutBase):
    pass

class InstitutRead(InstitutBase):
    id: int
    guvonoma: str

    class Config:
        orm_mode = True

class InstitutLocalizedOut(BaseModel):
    id: int
    malumot: str
    text: str
    guvonoma: str



# ==== Rahbariyat ====

class RahbariyatBase(BaseModel):
    ish_orni_uz: str
    ish_orni_ru: str
    ish_orni_en: str

    full_name_uz: str
    full_name_ru: str
    full_name_en: str

    qabul_kuni: date
    telefon: str
    email: EmailStr

    mutaxassisligi_uz: Optional[str] = None
    mutaxassisligi_ru: Optional[str] = None
    mutaxassisligi_en: Optional[str] = None

class RahbariyatCreate(RahbariyatBase):
    pass

class RahbariyatUpdate(BaseModel):
    ish_orni_uz: Optional[str] = None
    ish_orni_ru: Optional[str] = None
    ish_orni_en: Optional[str] = None


    full_name_uz: Optional[str] = None
    full_name_ru: Optional[str] = None
    full_name_en: Optional[str] = None

    qabul_kuni: Optional[date] = None
    telefon: Optional[str] = None
    email: Optional[EmailStr] = None

    mutaxassisligi_uz: Optional[str] = None
    mutaxassisligi_ru: Optional[str] = None
    mutaxassisligi_en: Optional[str] = None

class RahbariyatLocalizedOut(BaseModel):
    id: int
    ish_orni: str
    full_name: str
    qabul_kuni: date
    telefon: str
    email: str
    mutaxassisligi: str

class RahbariyatOut(RahbariyatBase):
    id: int

    class Config:
        orm_mode = True


# ==== Tashkiliy Tuzilma ====

class TashkiliyTuzilmaBase(BaseModel):
    desc_uz: str
    desc_ru: str
    desc_en: str

class TashkiliyTuzilmaCreate(TashkiliyTuzilmaBase):
    pass


class TashkiliyTuzilmaLocalizedOut(BaseModel):
    id: int
    desc: str
    tuzilma: str 


class TashkiliyTuzilmaRead(TashkiliyTuzilmaBase):
    id: int
    tuzilma: str

    class Config:
        orm_mode = True


# ==== Tarkibiy Bo‘linma ====

class TarkibiyBolinmaBase(BaseModel):
    ish_orni_uz: str
    ish_orni_ru: str
    ish_orni_en: str

    full_name: str


    telefon: str
    email: EmailStr

class TarkibiyBolinmaCreate(TarkibiyBolinmaBase):
    pass  # Fayl (rasm) UploadFile orqali

class TarkibiyBolinmaUpdate(BaseModel):
    ish_orni_uz: Optional[str] = None
    ish_orni_ru: Optional[str] = None
    ish_orni_en: Optional[str] = None

    full_name: Optional[str] = None


    telefon: Optional[str] = None
    email: Optional[EmailStr] = None


class TarkibiyBolinmaLocalizedOut(BaseModel):
    id: int
    ish_orni: str
    full_name: str
    telefon: str
    email: str
    rasm: str


class TarkibiyBolinmaOut(TarkibiyBolinmaBase):
    id: int
    rasm: str

    class Config:
        orm_mode = True
