from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.config.database import get_db_session
from app.config.settings import get_settings
from app.models.users import User

bearer_scheme = HTTPBearer()


def create_access_token(data: dict, expires_delta: timedelta = None):
    settings = get_settings()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db_session),
):
    settings = get_settings()

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные учётные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await crud.get_user(db, int(user_id))
    if user is None:
        raise credentials_exception
    return user


async def update_user(db: AsyncSession, user_id: int, data: schemas.UserUpdate):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        await db.commit()
    return user


async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user:
        await db.delete(user)
        await db.commit()
