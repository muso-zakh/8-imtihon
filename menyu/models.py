from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    menu_uz = Column(String(255), nullable=False)
    menu_ru = Column(String(255), nullable=False)
    menu_en = Column(String(255), nullable=False)



    submenus = relationship("Submenu", back_populates="menu", lazy="selectin")


class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(Integer, primary_key=True, index=True)
    submenu_uz = Column(String(255), nullable=False)
    submenu_ru = Column(String(255), nullable=False)
    submenu_en = Column(String(255), nullable=False)

    menu_id = Column(Integer, ForeignKey("menu.id"))

    menu = relationship("Menu", back_populates="submenus")
