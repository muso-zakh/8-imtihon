from fastapi import Depends, HTTPException, status
from core.deps import get_current_user


def superadmin_required(user=Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Faqat superadmin ruxsat etiladi."
        )
    return user


def admin_required(user=Depends(get_current_user)):
    if not (user.is_superuser or user.admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Faqat admin yoki superuser ruxsat etiladi."
        )
    return user
