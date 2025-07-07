from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from sqlalchemy.sql import func
from core.database import Base

class Elon(Base):
    __tablename__ = "elonlar"

    id = Column(Integer, primary_key=True, index=True)

    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)

    desc_uz = Column(Text, nullable=True)
    desc_ru = Column(Text, nullable=True)
    desc_en = Column(Text, nullable=True)

    rasm = Column(String(255), nullable=True)  # Fayl yo‘li

    created_at = Column(DateTime(timezone=True), server_default=func.now())



"""yangiliklar"""

class Yangilik(Base):
    __tablename__ = "yangiliklar"

    id = Column(Integer, primary_key=True, index=True)

    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)

    desc_uz = Column(Text, nullable=True)
    desc_ru = Column(Text, nullable=True)
    desc_en = Column(Text, nullable=True)

    rasm = Column(String(255), nullable=True)  # Fayl yo‘li
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    views_count = Column(Integer, default=0)





"""Uchrashuvlar"""

class Uchrashuv(Base):
    __tablename__ = "uchrashuvlar"

    id = Column(Integer, primary_key=True, index=True)

    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)

    desc_uz = Column(Text, nullable=True)
    desc_ru = Column(Text, nullable=True)
    desc_en = Column(Text, nullable=True)

    place_uz = Column(String(255), nullable=True)
    place_ru = Column(String(255), nullable=True)
    place_en = Column(String(255), nullable=True)

    date = Column(DateTime, nullable=False)  # uchrashuv sanasi-vaqti
    rasm = Column(String(255), nullable=True)  # fayl yo‘li (image path)




"""Ommaviy Tadbirlar"""


class Tadbir(Base):
    __tablename__ = "tadbirlar"

    id = Column(Integer, primary_key=True, index=True)

    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)

    desc_uz = Column(Text, nullable=True)
    desc_ru = Column(Text, nullable=True)
    desc_en = Column(Text, nullable=True)

    place_uz = Column(String(255), nullable=True)
    place_ru = Column(String(255), nullable=True)
    place_en = Column(String(255), nullable=True)

    date = Column(DateTime, nullable=False)  # Tadbir sanasi
    rasm = Column(String(255), nullable=True)  # Rasm fayl yo‘li (path or URL)



"""Xarqaro Hamkorlik"""

class XalqaroHamkorlik(Base):
    __tablename__ = "xalqaro_hamkorlik"

    id = Column(Integer, primary_key=True, index=True)

    hamkorliklar_uz = Column(String(255), nullable=False)
    hamkorliklar_ru = Column(String(255), nullable=False)
    hamkorliklar_en = Column(String(255), nullable=False)

    desc_uz = Column(Text, nullable=True)
    desc_ru = Column(Text, nullable=True)
    desc_en = Column(Text, nullable=True)

    rasm = Column(String(255), nullable=True)  # Fayl yo‘li yoki URL
    date = Column(DateTime, nullable=False)     # Hamkorlik sanasi




"""Seminar Korgazmalar"""

class SeminarKorgazma(Base):
    __tablename__ = "seminar_korgazmalar"

    id = Column(Integer, primary_key=True, index=True)

    nomi_uz = Column(String(255), nullable=False)
    nomi_ru = Column(String(255), nullable=False)
    nomi_en = Column(String(255), nullable=False)

    tavsif_uz = Column(Text, nullable=True)
    tavsif_ru = Column(Text, nullable=True)
    tavsif_en = Column(Text, nullable=True)

    datee = Column(Date, nullable=False)  # Foydalanuvchi 'YYYY-MM-DD' formatda kiritadi

    place_uz = Column(String(255), nullable=True)
    place_ru = Column(String(255), nullable=True)
    place_en = Column(String(255), nullable=True)

    tashkilotchi_uz = Column(String(255), nullable=True)
    tashkilotchi_ru = Column(String(255), nullable=True)
    tashkilotchi_en = Column(String(255), nullable=True)

    aloqa = Column(String(255), nullable=True)  # Telefon yoki email
    banner = Column(String(255), nullable=True)  # Fayl yo‘li yoki URL




"""Korrupsiya"""

class Korrupsiya(Base):
    __tablename__ = "korrupsiya"

    id = Column(Integer, primary_key=True, index=True)

    text_uz = Column(Text, nullable=True)
    text_ru = Column(Text, nullable=True)
    text_en = Column(Text, nullable=True)

    qonun_uz = Column(Text, nullable=True)
    qonun_ru = Column(Text, nullable=True)
    qonun_en = Column(Text, nullable=True)

    aloqa = Column(String(255), nullable=True)  # Telefon yoki email

    rasm = Column(String(255), nullable=True)  # Fayl yo‘li yoki URL
