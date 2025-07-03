from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os, shutil

from core.database import get_db
from core.deps import get_current_user
from .models import Institut, Rahbariyat, TashkiliyTuzilma, TarkibiyBolinma
from .schemas import (InstitutRead, RahbariyatCreate, RahbariyatUpdate, RahbariyatOut,
                      TashkiliyTuzilmaRead, TarkibiyBolinmaUpdate, TarkibiyBolinmaOut)

from fastapi.responses import FileResponse

router = APIRouter(prefix="/institut", tags=["Institut haqida"])
router2 = APIRouter(prefix="/rahbariyat", tags=["Rahbariyat"])
router3 = APIRouter(prefix="/tashkiliy_tuzilma", tags=["tashkiliy_tuzilma"])
router4 = APIRouter(prefix="/tarkibiy-bolinma", tags=["Tarkibiy_bolinma"])


UPLOAD_DIR = "uploads/pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=list[InstitutRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Institut))
    return result.scalars().all()

@router.post("/", response_model=InstitutRead)
async def create_institut(
    malumot: str,
    text: str,
    guvonoma: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    file_path = os.path.join(UPLOAD_DIR, guvonoma.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(guvonoma.file, buffer)

    item = Institut(malumot=malumot, text=text, guvonoma=file_path)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/pdf/{id}")
async def view_pdf(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Institut).where(Institut.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.guvonoma):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")
    return item.guvonoma


@router.delete("/{id}")
async def delete_institut(id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(Institut).where(Institut.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}



"""rahbariyat"""

@router2.get("/", response_model=list[RahbariyatOut])
async def get_all_rahbariyat(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rahbariyat))
    return result.scalars().all()

@router2.get("/{id}", response_model=RahbariyatOut)
async def get_rahbariyat_by_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rahbariyat).where(Rahbariyat.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return item

@router2.post("/", response_model=RahbariyatOut)
async def create_rahbariyat(
    data: RahbariyatCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    item = Rahbariyat(**data.dict())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router2.patch("/{id}", response_model=RahbariyatOut)
async def update_rahbariyat(
    id: int,
    data: RahbariyatUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Rahbariyat).where(Rahbariyat.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return item

@router2.delete("/{id}")
async def delete_rahbariyat(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Rahbariyat).where(Rahbariyat.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}



"""tashkiliy_tuzilma"""

UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router3.get("/", response_model=list[TashkiliyTuzilmaRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TashkiliyTuzilma))
    return result.scalars().all()

@router3.get("/{id}", response_model=TashkiliyTuzilmaRead)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TashkiliyTuzilma).where(TashkiliyTuzilma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return item

@router3.post("/", response_model=TashkiliyTuzilmaRead)
async def create_item(
    desc: str,
    tuzilma: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    file_path = os.path.join(UPLOAD_DIR, tuzilma.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(tuzilma.file, buffer)

    item = TashkiliyTuzilma(desc=desc, tuzilma=file_path)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router3.delete("/{id}")
async def delete_item(id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(TashkiliyTuzilma).where(TashkiliyTuzilma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    
    # Faylni ham o‘chiramiz
    if os.path.exists(item.tuzilma):
        os.remove(item.tuzilma)
    
    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}



"""tarkibiy bolinma"""

UPLOAD_DIR = "uploads/bolinma_rasmlar"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router4.get("/", response_model=list[TarkibiyBolinmaOut])
async def get_all_bolinmalar(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TarkibiyBolinma))
    return result.scalars().all()

@router4.get("/{id}", response_model=TarkibiyBolinmaOut)
async def get_bolinma_by_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TarkibiyBolinma).where(TarkibiyBolinma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return item

@router4.post("/", response_model=TarkibiyBolinmaOut)
async def create_bolinma(
    ish_orni: str,
    full_name: str,
    telefon: str,
    email: str,
    rasm: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, rasm.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(rasm.file, buffer)

    item = TarkibiyBolinma(
        ish_orni=ish_orni,
        full_name=full_name,
        telefon=telefon,
        email=email,
        rasm=file_path
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router4.patch("/{id}", response_model=TarkibiyBolinmaOut)
async def update_bolinma(
    id: int,
    data: TarkibiyBolinmaUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(TarkibiyBolinma).where(TarkibiyBolinma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return item

@router4.delete("/{id}")
async def delete_bolinma(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(TarkibiyBolinma).where(TarkibiyBolinma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    # Faylni ham o‘chirish mumkin (ixtiyoriy)
    if os.path.exists(item.rasm):
        os.remove(item.rasm)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}
