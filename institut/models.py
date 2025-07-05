from sqlalchemy import Column, Integer, String, Text, Date
from core.database import Base

# ------------------------
# Institut haqida
# ------------------------

class Institut(Base):
    __tablename__ = "institut_haqida"

    id = Column(Integer, primary_key=True, index=True)

    malumot_uz = Column(String(255))
    malumot_ru = Column(String(255))
    malumot_en = Column(String(255))

    text_uz = Column(Text)
    text_ru = Column(Text)
    text_en = Column(Text)

    guvonoma = Column(String(255))  # PDF file path


# ------------------------
# Rahbariyat
# ------------------------

class Rahbariyat(Base):
    __tablename__ = "rahbariyat"

    id = Column(Integer, primary_key=True, index=True)

    ish_orni_uz = Column(String, nullable=False)
    ish_orni_ru = Column(String, nullable=False)
    ish_orni_en = Column(String, nullable=False)

    full_name_uz = Column(String, nullable=False)
    full_name_ru = Column(String, nullable=False)
    full_name_en = Column(String, nullable=False)
    qabul_kuni = Column(Date, nullable=False)
    telefon = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    mutaxassisligi_uz = Column(String, nullable=True)
    mutaxassisligi_ru = Column(String, nullable=True)
    mutaxassisligi_en = Column(String, nullable=True)


# ------------------------
# Tashkiliy tuzilma
# ------------------------

class TashkiliyTuzilma(Base):
    __tablename__ = "tashkiliy_tuzilma"

    id = Column(Integer, primary_key=True, index=True)

    desc_uz = Column(String, nullable=False)
    desc_ru = Column(String, nullable=False)
    desc_en = Column(String, nullable=False)

    tuzilma = Column(String, nullable=False)  # Fayl nomi yoki URL


# ------------------------
# Tarkibiy bo‘linma
# ------------------------

class TarkibiyBolinma(Base):
    __tablename__ = "tarkibiy_bolinma"

    id = Column(Integer, primary_key=True, index=True)

    ish_orni_uz = Column(String, nullable=False)
    ish_orni_ru = Column(String, nullable=False)
    ish_orni_en = Column(String, nullable=False)

    full_name = Column(String, nullable=False)
    telefon = Column(String, nullable=False)
    email = Column(String, nullable=False)

    rasm = Column(String, nullable=False)
