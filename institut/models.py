from sqlalchemy import Column, Integer, String, Text
from core.database import Base

class Institut(Base):
    __tablename__ = "institut_haqida"

    id = Column(Integer, primary_key=True, index=True)
    malumot = Column(String(255))
    text = Column(Text)
    guvonoma = Column(String(255))  # PDF file path