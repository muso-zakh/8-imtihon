from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from core.deps import get_current_user
from .models import Menu, Submenu
from .schemas import (
    MenuCreate, MenuUpdate, MenuRead,
    SubmenuCreate, SubmenuUpdate, SubmenuRead
)
from sqlalchemy.orm import selectinload

from fastapi import Header

router5 = APIRouter(prefix="/menu", tags=["Menu"])

# --- MENU --- #


@router5.get("/")
async def get_all_menus(lang: str = Header(default="uz"), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Menu).options(selectinload(Menu.submenus)))
    menus = result.scalars().all()

    output = []
    for menu in menus:
        output.append({
            "id": menu.id,
            "menu": getattr(menu, f"menu_{lang}", menu.menu_uz),
            "submenus": [
                {
                    "id": sm.id,
                    "submenu": getattr(sm, f"submenu_{lang}", sm.submenu_uz),
                    "menu_id": sm.menu_id
                }
                for sm in menu.submenus
            ]
        })
    return output


@router5.get("/{id}")
async def get_menu(id: int, lang: str = Header(default="uz"), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Menu).options(selectinload(Menu.submenus)).where(Menu.id == id))
    menu = result.scalar_one_or_none()
    if not menu:
        raise HTTPException(status_code=404, detail="Topilmadi")

    return {
        "id": menu.id,
        "menu": getattr(menu, f"menu_{lang}", menu.menu_uz),
        "submenus": [
            {
                "id": sm.id,
                "submenu": getattr(sm, f"submenu_{lang}", sm.submenu_uz),
                "menu_id": sm.menu_id
            }
            for sm in menu.submenus
        ]
    }



@router5.post("/", response_model=MenuRead)
async def create_menu(
    data: MenuCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    item = Menu(**data.dict())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router5.patch("/{id}", response_model=MenuRead)
async def update_menu(
    id: int,
    data: MenuUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Menu).where(Menu.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return item


@router5.delete("/{id}")
async def delete_menu(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Menu).where(Menu.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    await db.delete(item)
    await db.commit()
    return {"detail": "Menu va unga tegishli submenular o‘chirildi"}


# --- SUBMENU --- #

@router5.post("/submenu/", response_model=SubmenuRead)
async def create_submenu(
    data: SubmenuCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    item = Submenu(**data.dict())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router5.patch("/submenu/{id}", response_model=SubmenuRead)
async def update_submenu(
    id: int,
    data: SubmenuUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Submenu).where(Submenu.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)
    
    await db.commit()
    await db.refresh(item)
    return item


@router5.delete("/submenu/{id}")
async def delete_submenu(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Submenu).where(Submenu.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    await db.delete(item)
    await db.commit()
    return {"detail": "Submenu o‘chirildi"}
