from pydantic import BaseModel, EmailStr
from datetime import date

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


"""rahbariyat"""

class RahbariyatBase(BaseModel):
    ish_orni: str
    full_name: str
    qabul_kuni: date
    telefon: str
    email: EmailStr
    mutaxassisligi: str | None = None  # optional

class RahbariyatCreate(RahbariyatBase):
    pass

class RahbariyatUpdate(BaseModel):
    ish_orni: str | None = None
    full_name: str | None = None
    qabul_kuni: date | None = None
    telefon: str | None = None
    email: EmailStr | None = None
    mutaxassisligi: str | None = None

class RahbariyatOut(RahbariyatBase):
    id: int

    class Config:
        orm_mode = True



"""tashkiliy_tuzilma"""

from pydantic import BaseModel

class TashkiliyTuzilmaBase(BaseModel):
    desc: str

class TashkiliyTuzilmaCreate(TashkiliyTuzilmaBase):
    pass  

class TashkiliyTuzilmaRead(TashkiliyTuzilmaBase):
    id: int
    tuzilma: str

    class Config:
        orm_mode = True



"""tarkibiy_bolinma"""

from pydantic import BaseModel, EmailStr
from typing import Optional

class TarkibiyBolinmaBase(BaseModel):
    ish_orni: str
    full_name: str
    telefon: str
    email: EmailStr

class TarkibiyBolinmaCreate(TarkibiyBolinmaBase):
    pass  # Fayl (rasm) alohida qo‘shiladi (FastAPI UploadFile orqali)

class TarkibiyBolinmaUpdate(BaseModel):
    ish_orni: Optional[str] = None
    full_name: Optional[str] = None
    telefon: Optional[str] = None
    email: Optional[EmailStr] = None

class TarkibiyBolinmaOut(TarkibiyBolinmaBase):
    id: int
    rasm: str

    class Config:
        orm_mode = True


