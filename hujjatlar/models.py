from sqlalchemy import Column, Integer, String, Text, Date
from core.database import Base

class Hujjatlar(Base):
    __tablename__ = "hujjatlar"

    id = Column(Integer, primary_key=True, index=True)
    guruhi = Column(String(255), nullable=False)           # Avvalgi ShNormaQoidalari guruhi
    desc = Column(Text, nullable=True)                     # Avvalgi ShNormaQoidalari desc
    shifr = Column(String(100), nullable=False)
    xujjat_nomi = Column(String(255), nullable=False)
    xavola = Column(String(255), nullable=False)           # PDF fayl manzili


"""standardlar"""

class Standartlar(Base):
    __tablename__ = "standartlar"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    created_at = Column(Date, nullable=False)
    desc = Column(Text, nullable=True)
    konsultatsiya = Column(Text, nullable=True)
    rasm = Column(String(255), nullable=True)