from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import FileResponse
import os, shutil
from datetime import datetime

from check_admin import admin_required

from core.database import get_db
from core.deps import get_current_user
from .models import Boglanish
from .schemas import (
    BoglanishCreate,
    BoglanishUpdate,
    BoglanishRead,
    BoglanishLocalizedOut
)

router19 = APIRouter(prefix="/boglanish", tags=["boglanish"])

UPLOAD_DIR = "uploads/boglanish"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_localized_fields(obj, lang: str):
    return {
        "id": obj.id,
        "full_name": getattr(obj, f"full_name_{lang}"),
        "email": obj.email,
        "telefon": obj.telefon,
        "sabab": getattr(obj, f"sabab_{lang}"),
        "text": getattr(obj, f"text_{lang}"),
        "fayl": obj.fayl,
        "created_at": obj.created_at,
    }


@router19.get("/", response_model=list[BoglanishLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db), user=Depends(admin_required)):
    result = await db.execute(select(Boglanish))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]


@router19.post("/", response_model=BoglanishRead)
async def create_item(
    full_name_uz: str,
    full_name_ru: str,
    full_name_en: str,
    email: str,
    telefon: str,
    sabab_uz: str,
    sabab_ru: str,
    sabab_en: str,
    text_uz: str,
    text_ru: str,
    text_en: str,
    fayl: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, fayl.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(fayl.file, buffer)

    item = Boglanish(
        full_name_uz=full_name_uz,
        full_name_ru=full_name_ru,
        full_name_en=full_name_en,
        email=email,
        telefon=telefon,
        sabab_uz=sabab_uz,
        sabab_ru=sabab_ru,
        sabab_en=sabab_en,
        text_uz=text_uz,
        text_ru=text_ru,
        text_en=text_en,
        fayl=file_path,
        created_at=datetime.utcnow()
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router19.get("/{id}", response_model=BoglanishLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db), user=Depends(admin_required)):
    result = await db.execute(select(Boglanish).where(Boglanish.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)


@router19.patch("/{id}", response_model=BoglanishLocalizedOut)
async def update_item(
    id: int,
    data: BoglanishUpdate,
    db: AsyncSession = Depends(get_db),
    # user=Depends(admin_required)
):
    result = await db.execute(select(Boglanish).where(Boglanish.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, "uz")


@router19.delete("/{id}")
async def delete_item(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(admin_required)
):
    result = await db.execute(select(Boglanish).where(Boglanish.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.fayl and os.path.exists(item.fayl):
        os.remove(item.fayl)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}


@router19.get("/download/{id}")
async def download_file(id: int, db: AsyncSession = Depends(get_db), user=Depends(admin_required)):
    result = await db.execute(select(Boglanish).where(Boglanish.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.fayl):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(
        path=item.fayl,
        filename=os.path.basename(item.fayl),
        media_type="application/octet-stream"
    )
