from sqlalchemy import Column, Integer, String, Text
from core.database import Base

class SertifikatlashtirishOrgan(Base):
    __tablename__ = "sertifikatlashtirish_organ"

    id = Column(Integer, primary_key=True, index=True)

    tavsif_uz = Column(Text, nullable=True)
    tavsif_ru = Column(Text, nullable=True)
    tavsif_en = Column(Text, nullable=True)

    xizmatlar_uz = Column(Text, nullable=True)
    xizmatlar_ru = Column(Text, nullable=True)
    xizmatlar_en = Column(Text, nullable=True)

    xizmatlar_desc_uz = Column(Text, nullable=True)
    xizmatlar_desc_ru = Column(Text, nullable=True)
    xizmatlar_desc_en = Column(Text, nullable=True)

    xolislik_siyosati_uz = Column(Text, nullable=True)
    xolislik_siyosati_ru = Column(Text, nullable=True)
    xolislik_siyosati_en = Column(Text, nullable=True)

    text_uz = Column(Text, nullable=True)
    text_ru = Column(Text, nullable=True)
    text_en = Column(Text, nullable=True)

    text_pdf = Column(String(255), nullable=True)  # Fayl yo‘li
