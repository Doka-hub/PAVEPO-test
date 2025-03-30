from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalars().first()


async def get_user_by_yandex_id(db: AsyncSession, yandex_id: str):
    result = await db.execute(select(models.User).where(models.User.yandex_id == yandex_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_data: dict):
    user = models.User(
        yandex_id=user_data.get("id"),
        email=user_data.get("default_email"),
        full_name=user_data.get("real_name"),
        is_superuser=False,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user_id: int, data: schemas.UserUpdate):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if user:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if user:
        await db.delete(user)
        await db.commit()
