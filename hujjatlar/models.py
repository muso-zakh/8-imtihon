from sqlalchemy import Column, Integer, String, Text, Date
from core.database import Base

class Hujjatlar(Base):
    __tablename__ = "hujjatlar"

    id = Column(Integer, primary_key=True, index=True)

    guruhi = Column(String(255), nullable=False)

    desc_uz = Column(Text, nullable=True)
    desc_ru = Column(Text, nullable=True)
    desc_en = Column(Text, nullable=True)

    shifr = Column(String(100), nullable=False)

    xujjat_nomi_uz = Column(String(255), nullable=False)
    xujjat_nomi_ru = Column(String(255), nullable=False)
    xujjat_nomi_en = Column(String(255), nullable=False)

    xavola = Column(String(255), nullable=False)         # PDF fayl manzili


"""standardlar"""

class Standartlar(Base):
    __tablename__ = "standartlar"

    id = Column(Integer, primary_key=True, index=True)

    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)

    desc_uz = Column(Text, nullable=True)
    desc_ru = Column(Text, nullable=True)
    desc_en = Column(Text, nullable=True)

    konsultatsiya_uz = Column(Text, nullable=True)
    konsultatsiya_ru = Column(Text, nullable=True)
    konsultatsiya_en = Column(Text, nullable=True)

    created_at = Column(Date, nullable=False)
    rasm = Column(String(255), nullable=True)



"""Qurilish Reglamentlar"""

class QurilishReglamentlar(Base):
    __tablename__ = "qurilish_reglamentlar"

    id = Column(Integer, primary_key=True, index=True)

    belgilanishi_uz = Column(String(255), nullable=False)
    belgilanishi_ru = Column(String(255), nullable=False)
    belgilanishi_en = Column(String(255), nullable=False)

    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)

    hujjat = Column(String(255), nullable=False)


    

"""Smeta Resurslar Nomi"""

class SmetaResurs(Base):
    __tablename__ = "smeta_resurs"

    id = Column(Integer, primary_key=True, index=True)

    new_shnq_raqam = Column(String(100), nullable=False)

    new_shnq_nomi_uz = Column(String(255), nullable=False)
    new_shnq_nomi_ru = Column(String(255), nullable=False)
    new_shnq_nomi_en = Column(String(255), nullable=False)

    shnq_raqam = Column(String(100), nullable=False)

    shnq_nomi_uz = Column(String(255), nullable=False)
    shnq_nomi_ru = Column(String(255), nullable=False)
    shnq_nomi_en = Column(String(255), nullable=False)

    fayl = Column(String(255), nullable=False)



"""Malumotnoma"""

class Malumotnoma(Base):
    __tablename__ = "malumotnoma"

    id = Column(Integer, primary_key=True, index=True)

    nomi_uz = Column(String(255), nullable=False)
    nomi_ru = Column(String(255), nullable=False)
    nomi_en = Column(String(255), nullable=False)

    hujjat = Column(String(255), nullable=False)