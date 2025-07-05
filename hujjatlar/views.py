from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import FileResponse
import os, shutil
from datetime import date

from core.database import get_db
from core.deps import get_current_user
from .models import Hujjatlar, Standartlar, QurilishReglamentlar, SmetaResurs, Malumotnoma
from .schemas import (HujjatCreate, HujjatlarLocalizedOut, HujjatUpdate, HujjatRead,
                       StandartRead, StandartUpdate, StandartLocalizedOut,
                       QurilishReglamentLocalizedOut, QurilishReglamentRead, QurilishReglamentUpdate,
                       SmetaResursLocalizedOut, SmetaResursRead, SmetaResursUpdate,
                       MalumotnomaRead, MalumotnomaUpdate, MalumotnomaLocalizedOut)

router6 = APIRouter(prefix="/hujjatlar", tags=["Hujjatlar"])
router8 = APIRouter(prefix="/qurilish-reglamentlar", tags=["Qurilish Reglamentlar"])
router9 = APIRouter(prefix="/smeta-resurs", tags=["SmetaResurs"])
router10 = APIRouter(prefix="/malumotnomalar", tags=["Malumotnomalar"])

UPLOAD_DIR = "uploads/hujjatlar"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router6.get("/", response_model=list[HujjatlarLocalizedOut])
async def get_all(
    lang: str = Query("uz", enum=["uz", "ru", "en"]),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Hujjatlar))
    items = result.scalars().all()
    return [
        {
            "id": item.id,
            "guruhi": item.guruhi,
            "desc": getattr(item, f"desc_{lang}"),
            "shifr": item.shifr,
            "xujjat_nomi": getattr(item, f"xujjat_nomi_{lang}"),
            "xavola": item.xavola,
        }
        for item in items
    ]


@router6.get("/{id}", response_model=HujjatlarLocalizedOut)
async def get_by_id(
    id: int,
    lang: str = Query("uz", enum=["uz", "ru", "en"]),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Hujjatlar).where(Hujjatlar.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return {
        "id": item.id,
        "guruhi": item.guruhi,
        "desc": getattr(item, f"desc_{lang}"),
        "shifr": item.shifr,
        "xujjat_nomi": getattr(item, f"xujjat_nomi_{lang}"),
        "xavola": item.xavola,
    }


@router6.post("/", response_model=HujjatRead)
async def create_hujjat(
    guruhi: str,
    shifr: str,
    xujjat_nomi_uz: str,
    xujjat_nomi_ru: str,
    xujjat_nomi_en: str,
    desc_uz: str = "",
    desc_ru: str = "",
    desc_en: str = "",
    fayl: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    file_path = os.path.join(UPLOAD_DIR, fayl.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(fayl.file, buffer)

    item = Hujjatlar(
        guruhi=guruhi,
        desc_uz=desc_uz,
        desc_ru=desc_ru,
        desc_en=desc_en,
        shifr=shifr,
        xujjat_nomi_uz=xujjat_nomi_uz,
        xujjat_nomi_ru=xujjat_nomi_ru,
        xujjat_nomi_en=xujjat_nomi_en,
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


def get_localized_fields(obj, lang):
    return {
        "id": obj.id,
        "title": getattr(obj, f"title_{lang}"),
        "created_at": obj.created_at,
        "desc": getattr(obj, f"desc_{lang}", None),
        "konsultatsiya": getattr(obj, f"konsultatsiya_{lang}", None),
        "rasm": obj.rasm,
    }


@router7.get("/", response_model=list[StandartLocalizedOut])
async def get_all_standartlar(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Standartlar))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]


@router7.get("/{id}", response_model=StandartLocalizedOut)
async def get_standart_by_id(id: int, lang: str = 'uz', db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Standartlar).where(Standartlar.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)


@router7.post("/", response_model=StandartRead)
async def create_standart(
    title_uz: str,
    title_ru: str,
    title_en: str,
    created_at: date,
    desc_uz: str = None,
    desc_ru: str = None,
    desc_en: str = None,
    konsultatsiya_uz: str = None,
    konsultatsiya_ru: str = None,
    konsultatsiya_en: str = None,
    rasm: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    file_path = os.path.join(UPLOAD_DIR, rasm.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(rasm.file, buffer)

    item = Standartlar(
        title_uz=title_uz,
        title_ru=title_ru,
        title_en=title_en,
        created_at=created_at,
        desc_uz=desc_uz,
        desc_ru=desc_ru,
        desc_en=desc_en,
        konsultatsiya_uz=konsultatsiya_uz,
        konsultatsiya_ru=konsultatsiya_ru,
        konsultatsiya_en=konsultatsiya_en,
        rasm=file_path,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router7.patch("/{id}", response_model=StandartLocalizedOut)
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
    return get_localized_fields(item, 'uz')


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




"""Qurilish Reglamentlar"""

UPLOAD_DIR = "uploads/qurilish_reglamentlar"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_localized_fields(obj, lang):
    return {
        "id": obj.id,
        "belgilanishi": getattr(obj, f"belgilanishi_{lang}"),
        "title": getattr(obj, f"title_{lang}"),
        "hujjat": obj.hujjat
    }

@router8.get("/", response_model=list[QurilishReglamentLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(QurilishReglamentlar))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]


@router8.get("/{id}", response_model=QurilishReglamentLocalizedOut)
async def get_by_id(id: int, lang: str = 'uz', db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(QurilishReglamentlar).where(QurilishReglamentlar.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)


@router8.post("/", response_model=QurilishReglamentRead)
async def create(
    belgilanishi_uz: str,
    belgilanishi_ru: str,
    belgilanishi_en: str,
    title_uz: str,
    title_ru: str,
    title_en: str,
    hujjat: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, hujjat.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(hujjat.file, buffer)

    item = QurilishReglamentlar(
        belgilanishi_uz=belgilanishi_uz,
        belgilanishi_ru=belgilanishi_ru,
        belgilanishi_en=belgilanishi_en,
        title_uz=title_uz,
        title_ru=title_ru,
        title_en=title_en,
        hujjat=file_path
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router8.patch("/{id}", response_model=QurilishReglamentLocalizedOut)
async def update(id: int, data: QurilishReglamentUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(QurilishReglamentlar).where(QurilishReglamentlar.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, 'uz')


@router8.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(QurilishReglamentlar).where(QurilishReglamentlar.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.hujjat and os.path.exists(item.hujjat):
        os.remove(item.hujjat)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}


@router8.get("/download/{id}")
async def download(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(QurilishReglamentlar).where(QurilishReglamentlar.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.hujjat):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(path=item.hujjat, filename=os.path.basename(item.hujjat), media_type="application/pdf")




"""Smeta Resurslar Nomi"""

UPLOAD_DIR = "uploads/smeta_resurs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_localized_fields(obj, lang):
    return {
        "id": obj.id,
        "new_shnq_raqam": obj.new_shnq_raqam,
        "new_shnq_nomi": getattr(obj, f"new_shnq_nomi_{lang}"),
        "shnq_raqam": obj.shnq_raqam,
        "shnq_nomi": getattr(obj, f"shnq_nomi_{lang}"),
        "fayl": obj.fayl,
    }


@router9.get("/", response_model=list[SmetaResursLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SmetaResurs))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]


@router9.get("/{id}", response_model=SmetaResursLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SmetaResurs).where(SmetaResurs.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)


@router9.post("/", response_model=SmetaResursRead)
async def create_smeta_resurs(
    new_shnq_raqam: str,
    new_shnq_nomi_uz: str,
    new_shnq_nomi_ru: str,
    new_shnq_nomi_en: str,
    shnq_raqam: str,
    shnq_nomi_uz: str,
    shnq_nomi_ru: str,
    shnq_nomi_en: str,
    fayl: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, fayl.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(fayl.file, buffer)

    item = SmetaResurs(
        new_shnq_raqam=new_shnq_raqam,
        new_shnq_nomi_uz=new_shnq_nomi_uz,
        new_shnq_nomi_ru=new_shnq_nomi_ru,
        new_shnq_nomi_en=new_shnq_nomi_en,
        shnq_raqam=shnq_raqam,
        shnq_nomi_uz=shnq_nomi_uz,
        shnq_nomi_ru=shnq_nomi_ru,
        shnq_nomi_en=shnq_nomi_en,
        fayl=file_path,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router9.patch("/{id}", response_model=SmetaResursLocalizedOut)
async def update_smeta_resurs(
    id: int,
    data: SmetaResursUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(SmetaResurs).where(SmetaResurs.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, "uz")


@router9.delete("/{id}")
async def delete_smeta_resurs(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(SmetaResurs).where(SmetaResurs.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.fayl and os.path.exists(item.fayl):
        os.remove(item.fayl)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}


@router9.get("/download/{id}")
async def download_file(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SmetaResurs).where(SmetaResurs.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.fayl):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(path=item.fayl, filename=os.path.basename(item.fayl), media_type="application/pdf")




"""Malumotnoma"""

UPLOAD_DIR = "uploads/malumotnomalar"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_localized_fields(obj, lang: str):
    return {
        "id": obj.id,
        "nomi": getattr(obj, f"nomi_{lang}"),
        "hujjat": obj.hujjat
    }


@router10.get("/", response_model=list[MalumotnomaLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Malumotnoma))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]


@router10.get("/{id}", response_model=MalumotnomaLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Malumotnoma).where(Malumotnoma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)


@router10.post("/", response_model=MalumotnomaRead)
async def create_malumotnoma(
    nomi_uz: str,
    nomi_ru: str,
    nomi_en: str,
    hujjat: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, hujjat.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(hujjat.file, buffer)

    item = Malumotnoma(
        nomi_uz=nomi_uz,
        nomi_ru=nomi_ru,
        nomi_en=nomi_en,
        hujjat=file_path,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router10.patch("/{id}", response_model=MalumotnomaLocalizedOut)
async def update_malumotnoma(
    id: int,
    data: MalumotnomaUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Malumotnoma).where(Malumotnoma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, "uz")


@router10.delete("/{id}")
async def delete_malumotnoma(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Malumotnoma).where(Malumotnoma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.hujjat and os.path.exists(item.hujjat):
        os.remove(item.hujjat)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}


@router10.get("/download/{id}")
async def download_file(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Malumotnoma).where(Malumotnoma.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.hujjat):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(
        path=item.hujjat,
        filename=os.path.basename(item.hujjat),
        media_type="application/pdf"
    )