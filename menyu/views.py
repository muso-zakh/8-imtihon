from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from core.deps import get_current_user
from .models import Menu
from .schemas import MenuCreate, MenuRead

router5 = APIRouter(prefix="/menu", tags=["Menyu"])

@router5.get("/", response_model=list[MenuRead])
async def get_all_menus(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Menu).order_by(Menu.order))
    return result.scalars().all()

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
    return {"detail": "O‘chirildi"}
