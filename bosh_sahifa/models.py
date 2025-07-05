from sqlalchemy import Column, Integer, String, Text
from core.database import Base

class BoshSahifa(Base):
    __tablename__ = "bosh_sahifa"

    id = Column(Integer, primary_key=True, index=True)

    # Tavsif (description) uch tilda
    tavsif_uz = Column(Text)
    tavsif_ru = Column(Text)
    tavsif_en = Column(Text)

    # SHNQ - shuningdek
    shnq_uz = Column(String(255))
    shnq_ru = Column(String(255))
    shnq_en = Column(String(255))

    # Standartlar matni
    standartlar_uz = Column(Text)
    standartlar_ru = Column(Text)
    standartlar_en = Column(Text)

    # Tashkilot nomi
    tashkilot_nomi_uz = Column(String(255))
    tashkilot_nomi_ru = Column(String(255))
    tashkilot_nomi_en = Column(String(255))

    # Rasm (barcha tillarda umumiy)
    rasm = Column(String(255))
