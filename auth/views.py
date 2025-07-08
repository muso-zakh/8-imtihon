from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from core.security import hash_password, verify_password, create_access_token

from auth.models import User
from auth.schemas import UserCreate, Token
from fastapi.security import OAuth2PasswordRequestForm

from check_admin import superadmin_required, admin_required

from .schemas import UserRead, UserCreate, LoginInput

from typing import Optional
from pydantic import EmailStr


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == user_data.email))).scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_superuser=False,
        admin=False
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer"}



@router.post("/login", response_model=Token)
async def login(data: LoginInput, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect credentials")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/", response_model=list[UserRead])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    user=Depends(superadmin_required)
):
    result = await db.execute(select(User))
    return result.scalars().all()



@router.patch("/{id}", response_model=UserRead)
async def update_user(
    id: int,
    email: Optional[EmailStr] = None,
    is_superuser: Optional[bool] = None,
    admin: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(superadmin_required)
):
    result = await db.execute(select(User).where(User.id == id))
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    if email:
        existing_user.email = email
    if is_superuser is not None:
        existing_user.is_superuser = is_superuser
    if admin is not None:
        existing_user.admin = admin

    await db.commit()
    await db.refresh(existing_user)
    return existing_user



@router.delete("/{id}")
async def delete_user(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(superadmin_required)
):
    result = await db.execute(select(User).where(User.id == id))
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    await db.delete(existing_user)
    await db.commit()
    return {"detail": "Foydalanuvchi o‘chirildi"}
