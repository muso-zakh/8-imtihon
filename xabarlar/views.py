from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import FileResponse
import os, shutil

from datetime import datetime, date

from core.database import get_db
from core.deps import get_current_user
from .models import Elon, Yangilik, Uchrashuv, Tadbir, XalqaroHamkorlik, SeminarKorgazma, Korrupsiya
from .schemas import (
    ElonCreate, ElonUpdate, ElonRead, ElonLocalizedOut,
    YangilikCreate, YangilikUpdate, YangilikRead, YangilikLocalizedOut,
    UchrashuvCreate, UchrashuvUpdate, UchrashuvRead, UchrashuvLocalizedOut,
    TadbirCreate, TadbirUpdate, TadbirRead, TadbirLocalizedOut,
    XalqaroHamkorlikCreate, XalqaroHamkorlikUpdate, XalqaroHamkorlikRead, XalqaroHamkorlikLocalizedOut,
    SeminarKorgazmaCreate, SeminarKorgazmaUpdate, SeminarKorgazmaRead, SeminarKorgazmaLocalizedOut,
    KorrupsiyaRead, KorrupsiyaUpdate, KorrupsiyaLocalizedOut
)

router12 = APIRouter(prefix="/elonlar", tags=["elonlar"])
router13 = APIRouter(prefix="/yangiliklar", tags=["yangiliklar"])
router14 = APIRouter(prefix="/uchrashuvlar", tags=["uchrashuvlar"])
router15 = APIRouter(prefix="/tadbirlar", tags=["tadbirlar"])
router16 = APIRouter(prefix="/xalqaro_hamkorlik", tags=["xalqaro_hamkorlik"])
router17 = APIRouter(prefix="/seminar-korgazmalar", tags=["seminar_korgazmalar"])
router18 = APIRouter(prefix="/korrupsiya", tags=["korrupsiya"])


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





"""Yangiliklar"""

UPLOAD_DIR = "uploads/yangiliklar"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_localized_fields(obj, lang: str):
    return {
        "id": obj.id,
        "title": getattr(obj, f"title_{lang}"),
        "desc": getattr(obj, f"desc_{lang}"),
        "rasm": obj.rasm,
        "created_at": obj.created_at,
        "views_count": obj.views_count,
    }



@router13.get("/", response_model=list[YangilikLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Yangilik))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]



@router13.post("/", response_model=YangilikRead)
async def create_yangilik(
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

    item = Yangilik(
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




@router13.get("/{id}", response_model=YangilikLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Yangilik).where(Yangilik.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    # views_count ni oshirish
    item.views_count += 1
    await db.commit()
    await db.refresh(item)

    return get_localized_fields(item, lang)



@router13.patch("/{id}", response_model=YangilikLocalizedOut)
async def update_yangilik(
    id: int,
    data: YangilikUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Yangilik).where(Yangilik.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, "uz")



@router13.delete("/{id}")
async def delete_yangilik(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Yangilik).where(Yangilik.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.rasm and os.path.exists(item.rasm):
        os.remove(item.rasm)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}



@router13.get("/download/{id}")
async def download_rasm(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Yangilik).where(Yangilik.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.rasm):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(
        path=item.rasm,
        filename=os.path.basename(item.rasm),
        media_type="image/jpeg"
    )





"""Uchrashuvlar"""

UPLOAD_DIR = "uploads/uchrashuvlar"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_localized_fields(obj, lang: str):
    return {
        "id": obj.id,
        "title": getattr(obj, f"title_{lang}"),
        "desc": getattr(obj, f"desc_{lang}"),
        "place": getattr(obj, f"place_{lang}"),
        "rasm": obj.rasm,
        "date": obj.date,
    }



@router14.get("/", response_model=list[UchrashuvLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Uchrashuv))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]



@router14.post("/", response_model=UchrashuvRead)
async def create_uchrashuv(
    title_uz: str,
    title_ru: str,
    title_en: str,
    desc_uz: str = "",
    desc_ru: str = "",
    desc_en: str = "",
    place_uz: str = "",
    place_ru: str = "",
    place_en: str = "",
    date: datetime = Form(...),  # ISO format: "2025-07-10T14:00:00"
    rasm: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, rasm.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(rasm.file, buffer)

    item = Uchrashuv(
        title_uz=title_uz,
        title_ru=title_ru,
        title_en=title_en,
        desc_uz=desc_uz,
        desc_ru=desc_ru,
        desc_en=desc_en,
        place_uz=place_uz,
        place_ru=place_ru,
        place_en=place_en,
        date=date,
        rasm=file_path
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item



@router14.get("/{id}", response_model=UchrashuvLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Uchrashuv).where(Uchrashuv.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    return get_localized_fields(item, lang)




@router14.patch("/{id}", response_model=UchrashuvLocalizedOut)
async def update_uchrashuv(
    id: int,
    data: UchrashuvUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Uchrashuv).where(Uchrashuv.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, "uz")



@router14.delete("/{id}")
async def delete_uchrashuv(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Uchrashuv).where(Uchrashuv.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.rasm and os.path.exists(item.rasm):
        os.remove(item.rasm)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}




@router14.get("/download/{id}")
async def download_rasm(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Uchrashuv).where(Uchrashuv.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.rasm):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(
        path=item.rasm,
        filename=os.path.basename(item.rasm),
        media_type="image/jpeg"
    )




"""Ommaviy Tadbirlar"""

UPLOAD_DIR = "uploads/tadbirlar"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_localized_fields(obj, lang: str):
    return {
        "id": obj.id,
        "title": getattr(obj, f"title_{lang}"),
        "desc": getattr(obj, f"desc_{lang}"),
        "place": getattr(obj, f"place_{lang}"),
        "rasm": obj.rasm,
        "date": obj.date,
    }



@router15.get("/", response_model=list[TadbirLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tadbir))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]


@router15.post("/", response_model=TadbirRead)
async def create_tadbir(
    title_uz: str = Form(...),
    title_ru: str = Form(...),
    title_en: str = Form(...),
    desc_uz: str = Form(""),
    desc_ru: str = Form(""),
    desc_en: str = Form(""),
    place_uz: str = Form(""),
    place_ru: str = Form(""),
    place_en: str = Form(""),
    date: datetime = Form(...),
    rasm: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, rasm.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(rasm.file, buffer)

    item = Tadbir(
        title_uz=title_uz,
        title_ru=title_ru,
        title_en=title_en,
        desc_uz=desc_uz,
        desc_ru=desc_ru,
        desc_en=desc_en,
        place_uz=place_uz,
        place_ru=place_ru,
        place_en=place_en,
        date=date,
        rasm=file_path
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router15.get("/{id}", response_model=TadbirLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tadbir).where(Tadbir.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)


@router15.patch("/{id}", response_model=TadbirLocalizedOut)
async def update_tadbir(
    id: int,
    data: TadbirUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Tadbir).where(Tadbir.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, "uz")


@router15.delete("/{id}")
async def delete_tadbir(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Tadbir).where(Tadbir.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.rasm and os.path.exists(item.rasm):
        os.remove(item.rasm)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}


@router15.get("/download/{id}")
async def download_rasm(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tadbir).where(Tadbir.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.rasm):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(
        path=item.rasm,
        filename=os.path.basename(item.rasm),
        media_type="image/jpeg"
    )




"""Xalqaro Hamkorlik"""

UPLOAD_DIR = "uploads/xalqaro_hamkorlik"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_localized_fields(obj, lang: str):
    return {
        "id": obj.id,
        "hamkorliklar": getattr(obj, f"hamkorliklar_{lang}"),
        "desc": getattr(obj, f"desc_{lang}"),
        "rasm": obj.rasm,
        "date": obj.date,
    }


@router16.get("/", response_model=list[XalqaroHamkorlikLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(XalqaroHamkorlik))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]


@router16.post("/", response_model=XalqaroHamkorlikRead)
async def create_item(
    hamkorliklar_uz: str,
    hamkorliklar_ru: str,
    hamkorliklar_en: str,
    desc_uz: str = "",
    desc_ru: str = "",
    desc_en: str = "",
    date: datetime = Form(...),
    rasm: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, rasm.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(rasm.file, buffer)

    item = XalqaroHamkorlik(
        hamkorliklar_uz=hamkorliklar_uz,
        hamkorliklar_ru=hamkorliklar_ru,
        hamkorliklar_en=hamkorliklar_en,
        desc_uz=desc_uz,
        desc_ru=desc_ru,
        desc_en=desc_en,
        rasm=file_path,
        date=date,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router16.get("/{id}", response_model=XalqaroHamkorlikLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(XalqaroHamkorlik).where(XalqaroHamkorlik.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)


@router16.patch("/{id}", response_model=XalqaroHamkorlikLocalizedOut)
async def update_item(
    id: int,
    data: XalqaroHamkorlikUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(XalqaroHamkorlik).where(XalqaroHamkorlik.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, "uz")


@router16.delete("/{id}")
async def delete_item(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(XalqaroHamkorlik).where(XalqaroHamkorlik.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.rasm and os.path.exists(item.rasm):
        os.remove(item.rasm)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}


@router16.get("/download/{id}")
async def download_rasm(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(XalqaroHamkorlik).where(XalqaroHamkorlik.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.rasm):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(
        path=item.rasm,
        filename=os.path.basename(item.rasm),
        media_type="image/jpeg"
    )




"""Seminar Korgazmalar"""

UPLOAD_DIR = "uploads/seminar_korgazmalar"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_localized_fields(obj, lang: str):
    return {
        "id": obj.id,
        "nomi": getattr(obj, f"nomi_{lang}"),
        "tavsif": getattr(obj, f"tavsif_{lang}"),
        "place": getattr(obj, f"place_{lang}"),
        "tashkilotchi": getattr(obj, f"tashkilotchi_{lang}"),
        "aloqa": obj.aloqa,
        "banner": obj.banner,
        "datee": obj.datee,
    }


@router17.get("/", response_model=list[SeminarKorgazmaLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SeminarKorgazma))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]


@router17.post("/", response_model=SeminarKorgazmaRead)
async def create_item(
    nomi_uz: str,
    nomi_ru: str,
    nomi_en: str,
    tavsif_uz: str,
    tavsif_ru: str,
    tavsif_en: str,
    place_uz: str,
    place_ru: str,
    place_en: str,
    tashkilotchi_uz: str,
    tashkilotchi_ru: str,
    tashkilotchi_en: str,
    aloqa: str,
    datee: date = Form(...),
    banner: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, banner.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(banner.file, buffer)

    item = SeminarKorgazma(
        nomi_uz=nomi_uz,
        nomi_ru=nomi_ru,
        nomi_en=nomi_en,
        tavsif_uz=tavsif_uz,
        tavsif_ru=tavsif_ru,
        tavsif_en=tavsif_en,
        place_uz=place_uz,
        place_ru=place_ru,
        place_en=place_en,
        tashkilotchi_uz=tashkilotchi_uz,
        tashkilotchi_ru=tashkilotchi_ru,
        tashkilotchi_en=tashkilotchi_en,
        aloqa=aloqa,
        banner=file_path,
        datee=datee,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router17.get("/{id}", response_model=SeminarKorgazmaLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SeminarKorgazma).where(SeminarKorgazma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)


@router17.patch("/{id}", response_model=SeminarKorgazmaLocalizedOut)
async def update_item(
    id: int,
    data: SeminarKorgazmaUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(SeminarKorgazma).where(SeminarKorgazma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, "uz")


@router17.delete("/{id}")
async def delete_item(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(SeminarKorgazma).where(SeminarKorgazma.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.banner and os.path.exists(item.banner):
        os.remove(item.banner)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}


@router17.get("/download/{id}")
async def download_banner(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SeminarKorgazma).where(SeminarKorgazma.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.banner):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(
        path=item.banner,
        filename=os.path.basename(item.banner),
        media_type="image/jpeg"
    )





"""Korrupsiya"""

UPLOAD_DIR = "uploads/korrupsiya"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_localized_fields(obj, lang: str):
    return {
        "id": obj.id,
        "text": getattr(obj, f"text_{lang}"),
        "qonun": getattr(obj, f"qonun_{lang}"),
        "aloqa": obj.aloqa,
        "rasm": obj.rasm,
    }

@router18.get("/", response_model=list[KorrupsiyaLocalizedOut])
async def get_all(lang: str = Query("uz", enum=["uz", "ru", "en"]), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Korrupsiya))
    items = result.scalars().all()
    return [get_localized_fields(item, lang) for item in items]

@router18.post("/", response_model=KorrupsiyaRead)
async def create_item(
    text_uz: str,
    text_ru: str,
    text_en: str,
    qonun_uz: str,
    qonun_ru: str,
    qonun_en: str,
    aloqa: str,
    rasm: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, rasm.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(rasm.file, buffer)

    item = Korrupsiya(
        text_uz=text_uz,
        text_ru=text_ru,
        text_en=text_en,
        qonun_uz=qonun_uz,
        qonun_ru=qonun_ru,
        qonun_en=qonun_en,
        aloqa=aloqa,
        rasm=file_path
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router18.get("/{id}", response_model=KorrupsiyaLocalizedOut)
async def get_by_id(id: int, lang: str = "uz", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Korrupsiya).where(Korrupsiya.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return get_localized_fields(item, lang)

@router18.patch("/{id}", response_model=KorrupsiyaLocalizedOut)
async def update_item(
    id: int,
    data: KorrupsiyaUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Korrupsiya).where(Korrupsiya.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return get_localized_fields(item, "uz")

@router18.delete("/{id}")
async def delete_item(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Korrupsiya).where(Korrupsiya.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Topilmadi")

    if item.rasm and os.path.exists(item.rasm):
        os.remove(item.rasm)

    await db.delete(item)
    await db.commit()
    return {"detail": "O‘chirildi"}

@router18.get("/download/{id}")
async def download_rasm(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Korrupsiya).where(Korrupsiya.id == id))
    item = result.scalar_one_or_none()
    if not item or not os.path.exists(item.rasm):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(
        path=item.rasm,
        filename=os.path.basename(item.rasm),
        media_type="image/jpeg"
    )