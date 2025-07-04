from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import FileResponse
import os, shutil
from datetime import date

from core.database import get_db
from core.deps import get_current_user
from .models import Hujjatlar, Standartlar
from .schemas import HujjatCreate, HujjatUpdate, HujjatRead, StandartRead, StandartUpdate, StandartCreate

router6 = APIRouter(prefix="/hujjatlar", tags=["Hujjatlar"])

UPLOAD_DIR = "uploads/hujjatlar"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router6.get("/", response_model=list[HujjatRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hujjatlar))
    return result.scalars().all()


@router6.get("/{id}", response_model=HujjatRead)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hujjatlar).where(Hujjatlar.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return item


@router6.post("/", response_model=HujjatRead)
async def create_hujjat(
    guruhi: str,
    shifr: str,
    xujjat_nomi: str,
    desc: str = None,
    fayl: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    file_path = os.path.join(UPLOAD_DIR, fayl.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(fayl.file, buffer)

    # Fayl manzili `xavola` sifatida saqlanadi
    item = Hujjatlar(
        guruhi=guruhi,
        desc=desc,
        shifr=shifr,
        xujjat_nomi=xujjat_nomi,
        xavola=file_path,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router6.patch("/{id}", response_model=HujjatRead)
async def update_hujjat(
    id: int,
    data: HujjatUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Hujjatlar).where(Hujjatlar.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return item


@router6.delete("/{id}")
async def delete_hujjat(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Hujjatlar).where(Hujjatlar.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    # Faylni o‘chiramiz
    if item.xavola and os.path.exists(item.xavola):
        os.remove(item.xavola)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}


@router6.get("/download/{id}")
async def download_file(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hujjatlar).where(Hujjatlar.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.xavola):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(path=item.xavola, filename=os.path.basename(item.xavola), media_type="application/pdf")


"""standardlar"""

router7 = APIRouter(prefix="/standartlar", tags=["Standartlar"])

UPLOAD_DIR = "uploads/standart_rasmlar"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router7.get("/", response_model=list[StandartRead])
async def get_all_standartlar(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Standartlar))
    return result.scalars().all()


@router7.get("/{id}", response_model=StandartRead)
async def get_standart_by_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Standartlar).where(Standartlar.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return item


@router7.post("/", response_model=StandartRead)
async def create_standart(
    title: str,
    created_at: date,
    desc: str = None,
    konsultatsiya: str = None,
    rasm: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    file_path = os.path.join(UPLOAD_DIR, rasm.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(rasm.file, buffer)

    item = Standartlar(
        title=title,
        created_at=created_at,
        desc=desc,
        konsultatsiya=konsultatsiya,
        rasm=file_path,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router7.patch("/{id}", response_model=StandartRead)
async def update_standart(
    id: int,
    data: StandartUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Standartlar).where(Standartlar.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return item


@router7.delete("/{id}")
async def delete_standart(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Standartlar).where(Standartlar.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.rasm and os.path.exists(item.rasm):
        os.remove(item.rasm)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}


@router7.get("/download/{id}")
async def download_rasm(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Standartlar).where(Standartlar.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.rasm):
        raise HTTPException(status_code=404, detail="Rasm topilmadi")

    return FileResponse(path=item.rasm, filename=os.path.basename(item.rasm), media_type="image/*")
