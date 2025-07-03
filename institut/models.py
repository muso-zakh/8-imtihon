from sqlalchemy import Column, Integer, String, Text, Date
from core.database import Base

class Institut(Base):
    __tablename__ = "institut_haqida"

    id = Column(Integer, primary_key=True, index=True)
    malumot = Column(String(255))
    text = Column(Text)
    guvonoma = Column(String(255))  # PDF file path


"""rahbariyat"""

class Rahbariyat(Base):
    __tablename__ = "rahbariyat"

    id = Column(Integer, primary_key=True, index=True)
    ish_orni = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    qabul_kuni = Column(Date, nullable=False)
    telefon = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    mutaxassisligi = Column(String, nullable=True)



"""tashkiliy_tuzilma"""

class TashkiliyTuzilma(Base):
    __tablename__ = "tashkiliy_tuzilma"

    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String, nullable=False)
    tuzilma = Column(String, nullable=False) 


"""tarkibiy_bolinma"""

class TarkibiyBolinma(Base):
    __tablename__ = "tarkibiy_bolinma"

    id = Column(Integer, primary_key=True, index=True)
    ish_orni = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    telefon = Column(String, nullable=False)
    email = Column(String, nullable=False)
    rasm = Column(String, nullable=False)