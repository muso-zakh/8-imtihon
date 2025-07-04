from sqlalchemy import Column, Integer, String
from core.database import Base

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)       # Menyu sarlavhasi
    url = Column(String(255), nullable=False)          # Menyu yo‘li (masalan: "/yangiliklar")
    order = Column(Integer, default=0)                 # Menyu tartibi
