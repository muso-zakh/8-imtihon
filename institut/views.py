from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os, shutil

from fastapi.responses import JSONResponse
from starlette.requests import Request

from core.database import get_db
from core.deps import get_current_user
from .models import Institut
from .schemas import InstitutRead

from fastapi.responses import FileResponse

router = APIRouter(prefix="/institut", tags=["Institut haqida"])

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
