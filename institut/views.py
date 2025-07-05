from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os, shutil

from datetime import datetime

from core.database import get_db
from core.deps import get_current_user
from .models import Institut,  Rahbariyat, TashkiliyTuzilma, TarkibiyBolinma
from .schemas import (InstitutRead, InstitutLocalizedOut, 
                      RahbariyatLocalizedOut, RahbariyatCreate, RahbariyatUpdate, RahbariyatOut,
                      TashkiliyTuzilmaLocalizedOut, TashkiliyTuzilmaRead, TarkibiyBolinmaUpdate, TarkibiyBolinmaOut, TarkibiyBolinmaLocalizedOut)

from fastapi.responses import FileResponse

router = APIRouter(prefix="/institut", tags=["Institut haqida"])
router2 = APIRouter(prefix="/rahbariyat", tags=["Rahbariyat"])
router3 = APIRouter(prefix="/tashkiliy_tuzilma", tags=["tashkiliy_tuzilma"])
router4 = APIRouter(prefix="/tarkibiy-bolinma", tags=["Tarkibiy_bolinma"])


PDF_UPLOAD = "uploads/pdfs"
IMG_UPLOAD = "uploads/images"
BOLINMA_UPLOAD = "uploads/bolinma_rasmlar"
for path in [PDF_UPLOAD, IMG_UPLOAD, BOLINMA_UPLOAD]:
    os.makedirs(path, exist_ok=True)

@router.get("/", response_model=list[InstitutLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Institut))
    items = result.scalars().all()
    return [
        {
            "id": item.id,
            "malumot": getattr(item, f"malumot_{lang}"),
            "text": getattr(item, f"text_{lang}"),
            "guvonoma": item.guvonoma
        }
        for item in items
    ]

@router.post("/", response_model=InstitutRead)
async def create_institut(
    malumot_uz: str,
    malumot_ru: str,
    malumot_en: str,
    text_uz: str,
    text_ru: str,
    text_en: str,
    guvonoma: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    path = os.path.join(PDF_UPLOAD, guvonoma.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(guvonoma.file, buffer)

    item = Institut(
        malumot_uz=malumot_uz,
        malumot_ru=malumot_ru,
        malumot_en=malumot_en,
        text_uz=text_uz,
        text_ru=text_ru,
        text_en=text_en,
        guvonoma=path
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router.get("/pdf/{id}")
async def view_pdf(
    id: int,
    lang: str = Query("uz", enum=["uz", "ru", "en"]),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Institut).where(Institut.id == id))
    item = result.scalar_one_or_none()

    if not item or not os.path.exists(item.guvonoma):
        # Uch til uchun xabarlar
        messages = {
            "uz": "Fayl topilmadi",
            "ru": "Файл не найден",
            "en": "File not found"
        }
        raise HTTPException(
            status_code=404,
            detail=messages.get(lang, messages["uz"])
        )

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

@router2.get("/", response_model=list[RahbariyatLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rahbariyat))
    items = result.scalars().all()
    return [
        {
            "id": item.id,
            "ish_orni": getattr(item, f"ish_orni_{lang}"),
            "full_name": getattr(item, f"full_name_{lang}"),
            "qabul_kuni": item.qabul_kuni,
            "telefon": item.telefon,
            "email": item.email,
            "mutaxassisligi": getattr(item, f"mutaxassisligi_{lang}") if getattr(item, f"mutaxassisligi_{lang}", None) else None
        }
        for item in items
    ]

@router2.get("/{id}", response_model=RahbariyatLocalizedOut)
async def get_rahbariyat_by_id(id: int, lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rahbariyat).where(Rahbariyat.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return {
        "id": item.id,
        "ish_orni": getattr(item, f"ish_orni_{lang}"),
        "full_name": getattr(item, f"full_name_{lang}"),
        "qabul_kuni": item.qabul_kuni,
        "telefon": item.telefon,
        "email": item.email,
        "mutaxassisligi": getattr(item, f"mutaxassisligi_{lang}", None)
    }

@router2.post("/", response_model=RahbariyatOut)
async def create(
    ish_orni_uz: str,
    ish_orni_ru: str,
    ish_orni_en: str,
    full_name_uz: str,
    full_name_ru: str,
    full_name_en: str,
    qabul_kuni: str,  # kelayotgan qiymat str bo'ladi
    telefon: str,
    email: str,
    mutaxassisligi_uz: str = "",
    mutaxassisligi_ru: str = "",
    mutaxassisligi_en: str = "",
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        # ✅ str -> datetime.date
        qabul_kuni_date = datetime.strptime(qabul_kuni, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="qabul_kuni noto‘g‘ri formatda. To‘g‘ri format: YYYY-MM-DD")

    item = Rahbariyat(
        ish_orni_uz=ish_orni_uz,
        ish_orni_ru=ish_orni_ru,
        ish_orni_en=ish_orni_en,
        full_name_uz = full_name_uz,
        full_name_ru = full_name_ru,
        full_name_en = full_name_en,
        qabul_kuni=qabul_kuni_date,  # 👈 bu yerda date tip uzatiladi
        telefon=telefon,
        email=email,
        mutaxassisligi_uz=mutaxassisligi_uz,
        mutaxassisligi_ru=mutaxassisligi_ru,
        mutaxassisligi_en=mutaxassisligi_en
    )
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

@router3.get("/", response_model=list[TashkiliyTuzilmaLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TashkiliyTuzilma))
    items = result.scalars().all()
    return [
        {
            "id": item.id,
            "desc": getattr(item, f"desc_{lang}"),
            "tuzilma": item.tuzilma
        }
        for item in items
    ]

@router3.get("/{id}", response_model=TashkiliyTuzilmaLocalizedOut)
async def get_by_id(id: int, lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TashkiliyTuzilma).where(TashkiliyTuzilma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return {
        "id": item.id,
        "desc": getattr(item, f"desc_{lang}"),
        "tuzilma": item.tuzilma
    }

@router3.post("/", response_model=TashkiliyTuzilmaRead)
async def create(
    desc_uz: str,
    desc_ru: str,
    desc_en: str,
    tuzilma: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    path = os.path.join(IMG_UPLOAD, tuzilma.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(tuzilma.file, buffer)

    item = TashkiliyTuzilma(
        desc_uz=desc_uz,
        desc_ru=desc_ru,
        desc_en=desc_en,
        tuzilma=path
    )
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


@router4.get("/", response_model=list[TarkibiyBolinmaLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TarkibiyBolinma))
    items = result.scalars().all()
    return [
        {
            "id": item.id,
            "ish_orni": getattr(item, f"ish_orni_{lang}"),
            "full_name": item.full_name,
            "telefon": item.telefon,
            "email": item.email,
            "rasm": item.rasm
        }
        for item in items
    ]

@router4.get("/{id}", response_model=TarkibiyBolinmaLocalizedOut)
async def get_bolinma_by_id(id: int, lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TarkibiyBolinma).where(TarkibiyBolinma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return {
        "id": item.id,
        "ish_orni": getattr(item, f"ish_orni_{lang}"),
        "full_name": item.full_name,
        "telefon": item.telefon,
        "email": item.email,
        "rasm": item.rasm
    }

@router4.post("/", response_model=TarkibiyBolinmaOut)
async def create(
    ish_orni_uz: str,
    ish_orni_ru: str,
    ish_orni_en: str,
    full_name: str,
    telefon: str,
    email: str,
    rasm: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    path = os.path.join(BOLINMA_UPLOAD, rasm.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(rasm.file, buffer)

    item = TarkibiyBolinma(
        ish_orni_uz=ish_orni_uz,
        ish_orni_ru=ish_orni_ru,
        ish_orni_en=ish_orni_en,
        full_name=full_name,
        telefon=telefon,
        email=email,
        rasm=path
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
