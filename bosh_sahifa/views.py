from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from core.deps import get_current_superuser, get_current_user
from .models import BoshSahifa
from .schemas import BoshSahifaCreate, BoshSahifaRead

router = APIRouter(prefix="/bosh_sahifa", tags=["Bosh sahifa"])

@router.get("/", response_model=list[BoshSahifaRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BoshSahifa))
    return result.scalars().all()

@router.post("/", response_model=BoshSahifaRead)
async def create(data: BoshSahifaCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    item = BoshSahifa(**data.dict())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(BoshSahifa).where(BoshSahifa.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(item)
    await db.commit()
    return {"detail": "Deleted"}