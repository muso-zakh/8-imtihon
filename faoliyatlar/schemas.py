from pydantic import BaseModel
from typing import Optional


class SertifikatlashtirishOrganBase(BaseModel):
    tavsif_uz: Optional[str] = None
    tavsif_ru: Optional[str] = None
    tavsif_en: Optional[str] = None

    xizmatlar_uz: Optional[str] = None
    xizmatlar_ru: Optional[str] = None
    xizmatlar_en: Optional[str] = None

    xizmatlar_desc_uz: Optional[str] = None
    xizmatlar_desc_ru: Optional[str] = None
    xizmatlar_desc_en: Optional[str] = None

    xolislik_siyosati_uz: Optional[str] = None
    xolislik_siyosati_ru: Optional[str] = None
    xolislik_siyosati_en: Optional[str] = None

    text_uz: Optional[str] = None
    text_ru: Optional[str] = None
    text_en: Optional[str] = None

    text_pdf: Optional[str] = None  # Fayl yo‘li yoki nomi


class SertifikatlashtirishOrganCreate(SertifikatlashtirishOrganBase):
    pass


class SertifikatlashtirishOrganUpdate(BaseModel):
    tavsif_uz: Optional[str] = None
    tavsif_ru: Optional[str] = None
    tavsif_en: Optional[str] = None

    xizmatlar_uz: Optional[str] = None
    xizmatlar_ru: Optional[str] = None
    xizmatlar_en: Optional[str] = None

    xizmatlar_desc_uz: Optional[str] = None
    xizmatlar_desc_ru: Optional[str] = None
    xizmatlar_desc_en: Optional[str] = None

    xolislik_siyosati_uz: Optional[str] = None
    xolislik_siyosati_ru: Optional[str] = None
    xolislik_siyosati_en: Optional[str] = None

    text_uz: Optional[str] = None
    text_ru: Optional[str] = None
    text_en: Optional[str] = None

    text_pdf: Optional[str] = None


class SertifikatlashtirishOrganRead(SertifikatlashtirishOrganBase):
    id: int

    class Config:
        orm_mode = True


class SertifikatlashtirishOrganLocalizedOut(BaseModel):
    id: int
    tavsif: Optional[str] = None
    xizmatlar: Optional[str] = None
    xizmatlar_desc: Optional[str] = None
    xolislik_siyosati: Optional[str] = None
    text: Optional[str] = None
    text_pdf: Optional[str] = None

    class Config:
        orm_mode = True
