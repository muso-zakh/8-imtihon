from sqlalchemy import Column, Integer, String, DateTime
from core.database import Base
from datetime import datetime


class Boglanish(Base):
    __tablename__ = "boglanishlar"

    id = Column(Integer, primary_key=True, index=True)

    full_name_uz = Column(String(255), nullable=True)
    full_name_ru = Column(String(255), nullable=True)
    full_name_en = Column(String(255), nullable=True)

    email = Column(String(255), nullable=True)
    telefon = Column(String(100), nullable=True)

    sabab_uz = Column(String(255), nullable=True)
    sabab_ru = Column(String(255), nullable=True)
    sabab_en = Column(String(255), nullable=True)

    text_uz = Column(String, nullable=True)
    text_ru = Column(String, nullable=True)
    text_en = Column(String, nullable=True)

    fayl = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)  
