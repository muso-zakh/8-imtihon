from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import FileResponse
import os, shutil

from core.database import get_db
from core.deps import get_current_user
from .models import Elon
from .schemas import (
    ElonCreate,
    ElonUpdate,
    ElonRead,
    ElonLocalizedOut
)

router12 = APIRouter(prefix="/elonlar", tags=["elonlar"])

UPLOAD_DIR = "uploads/elonlar"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_localized_fields(obj, lang: str):
    return {
        "id": obj.id,
        "title": getattr(obj, f"title_{lang}"),
        "desc": getattr(obj, f"desc_{lang}"),
        "rasm": obj.rasm,
        "created_at": obj.created_at,
    }


@router12.get("/", response_model=list[ElonLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Elon))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]



@router12.post("/", response_model=ElonRead)
async def create_elon(
    title_uz: str,
    title_ru: str,
    title_en: str,
    desc_uz: str = "",
    desc_ru: str = "",
    desc_en: str = "",
    rasm: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, rasm.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(rasm.file, buffer)

    item = Elon(
        title_uz=title_uz,
        title_ru=title_ru,
        title_en=title_en,
        desc_uz=desc_uz,
        desc_ru=desc_ru,
        desc_en=desc_en,
        rasm=file_path
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item



@router12.get("/{id}", response_model=ElonLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Elon).where(Elon.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)


@router12.get("/{id}", response_model=ElonLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Elon).where(Elon.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)



@router12.patch("/{id}", response_model=ElonLocalizedOut)
async def update_elon(
    id: int,
    data: ElonUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Elon).where(Elon.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, "uz")


@router12.delete("/{id}")
async def delete_elon(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Elon).where(Elon.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.rasm and os.path.exists(item.rasm):
        os.remove(item.rasm)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}



@router12.get("/download/{id}")
async def download_rasm(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Elon).where(Elon.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.rasm):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(
        path=item.rasm,
        filename=os.path.basename(item.rasm),
        media_type="image/jpeg"
    )



