from pydantic import BaseModel
from typing import Optional, List


# Base schema for Menu with multilingual fields
class MenuBase(BaseModel):
    menu_uz: str
    menu_ru: str
    menu_en: str



class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    menu_uz: Optional[str] = None
    menu_ru: Optional[str] = None
    menu_en: Optional[str] = None


class MenuRead(MenuBase):
    id: int

    class Config:
        orm_mode = True


# Base schema for Submenu with multilingual fields
class SubmenuBase(BaseModel):
    submenu_uz: str
    submenu_ru: str
    submenu_en: str


class SubmenuCreate(SubmenuBase):
    menu_id: int


class SubmenuUpdate(BaseModel):
    submenu_uz: Optional[str] = None
    submenu_ru: Optional[str] = None
    submenu_en: Optional[str] = None
    menu_id: Optional[int] = None


class SubmenuRead(SubmenuBase):
    id: int
    menu_id: int

    class Config:
        orm_mode = True
