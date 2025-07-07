from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import FileResponse
import os, shutil

from check_admin import admin_required

from core.database import get_db
from core.deps import get_current_user
from .models import SertifikatlashtirishOrgan
from .schemas import (
    SertifikatlashtirishOrganCreate,
    SertifikatlashtirishOrganUpdate,
    SertifikatlashtirishOrganRead,
    SertifikatlashtirishOrganLocalizedOut
)

router11 = APIRouter(prefix="/faoliyat", tags=["faoliyat"])


UPLOAD_DIR = "uploads/sertifikatlashtirish_organ"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_localized_fields(obj, lang: str):
    return {
        "id": obj.id,
        "tavsif": getattr(obj, f"tavsif_{lang}"),
        "xizmatlar": getattr(obj, f"xizmatlar_{lang}"),
        "xizmatlar_desc": getattr(obj, f"xizmatlar_desc_{lang}"),
        "xolislik_siyosati": getattr(obj, f"xolislik_siyosati_{lang}"),
        "text": getattr(obj, f"text_{lang}"),
        "text_pdf": obj.text_pdf,
    }





@router11.get("/", response_model=list[SertifikatlashtirishOrganLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SertifikatlashtirishOrgan))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]



@router11.post("/", response_model=SertifikatlashtirishOrganRead)
async def create_item(
    tavsif_uz: str = "",
    tavsif_ru: str = "",
    tavsif_en: str = "",
    xizmatlar_uz: str = "",
    xizmatlar_ru: str = "",
    xizmatlar_en: str = "",
    xizmatlar_desc_uz: str = "",
    xizmatlar_desc_ru: str = "",
    xizmatlar_desc_en: str = "",
    xolislik_siyosati_uz: str = "",
    xolislik_siyosati_ru: str = "",
    xolislik_siyosati_en: str = "",
    text_uz: str = "",
    text_ru: str = "",
    text_en: str = "",
    text_pdf: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(admin_required)
):
    file_path = os.path.join(UPLOAD_DIR, text_pdf.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(text_pdf.file, buffer)

    item = SertifikatlashtirishOrgan(
        tavsif_uz=tavsif_uz, tavsif_ru=tavsif_ru, tavsif_en=tavsif_en,
        xizmatlar_uz=xizmatlar_uz, xizmatlar_ru=xizmatlar_ru, xizmatlar_en=xizmatlar_en,
        xizmatlar_desc_uz=xizmatlar_desc_uz, xizmatlar_desc_ru=xizmatlar_desc_ru, xizmatlar_desc_en=xizmatlar_desc_en,
        xolislik_siyosati_uz=xolislik_siyosati_uz, xolislik_siyosati_ru=xolislik_siyosati_ru, xolislik_siyosati_en=xolislik_siyosati_en,
        text_uz=text_uz, text_ru=text_ru, text_en=text_en,
        text_pdf=file_path,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item



@router11.get("/{id}", response_model=SertifikatlashtirishOrganLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SertifikatlashtirishOrgan).where(SertifikatlashtirishOrgan.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)


@router11.patch("/{id}", response_model=SertifikatlashtirishOrganLocalizedOut)
async def update_item(
    id: int,
    data: SertifikatlashtirishOrganUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(admin_required)
):
    result = await db.execute(select(SertifikatlashtirishOrgan).where(SertifikatlashtirishOrgan.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, "uz")



@router11.delete("/{id}")
async def delete_item(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(admin_required)
):
    result = await db.execute(select(SertifikatlashtirishOrgan).where(SertifikatlashtirishOrgan.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.text_pdf and os.path.exists(item.text_pdf):
        os.remove(item.text_pdf)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}


@router11.get("/download/{id}")
async def download_file(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SertifikatlashtirishOrgan).where(SertifikatlashtirishOrgan.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.text_pdf):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(
        path=item.text_pdf,
        filename=os.path.basename(item.text_pdf),
        media_type="application/pdf"
    )
