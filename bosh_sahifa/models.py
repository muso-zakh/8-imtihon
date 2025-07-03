from sqlalchemy import Column, Integer, String, Text
from core.database import Base

class BoshSahifa(Base):
    __tablename__ = "bosh_sahifa"

    id = Column(Integer, primary_key=True, index=True)
    tavsif = Column(Text)
    SHNQ = Column(String(255))
    standartlar = Column(Text)
    tashkilot_nomi = Column(String(255))
    rasm = Column(String(255))