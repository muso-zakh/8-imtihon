from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import get_db
from core.security import JWT_SECRET, ALGORITHM
from auth.models import User
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
# from core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise credentials_exception

    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

async def get_current_superuser(user: User = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Only admins")
    return user









# """"""
# bearer_scheme = HTTPBearer()

# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
#     db: Session = Depends(get_db)
# ) -> User:
#     token = credentials.credentials
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Token noto‘g‘ri yoki muddati tugagan",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         email: Optional[str] = payload.get("sub")
#         user_id: Optional[int] = payload.get("user_id")
#         if email is None or user_id is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = db.query(User).filter(User.id == user_id).first()
#     if user is None or not user.is_active:
#         raise credentials_exception
#     return user



# from datetime import datetime, timedelta

# from fastapi import Depends, HTTPException, status
# from jose import JWTError, jwt
# from passlib.context import CryptContext

# from core.database import get_db
# from models.user import User, UserRole
# from schemas.user import TokenData

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# bearer_scheme = HTTPBearer()

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

