from sqlalchemy import Column, Integer, String, Text, DateTime
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
