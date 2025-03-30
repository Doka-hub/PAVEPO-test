from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.config.database import get_db_session
from app.services import get_current_user, update_user, delete_user

router = APIRouter()


@router.get("/me", response_model=schemas.User)
async def user_retrieve(
    current_user: schemas.User = Depends(get_current_user),
):
    return current_user


@router.put("/me", response_model=schemas.User)
async def user_update(
    user_data: schemas.UserUpdate,
    current_user: schemas.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    updated_user = await update_user(db, current_user.id, user_data)
    return updated_user


@router.delete("/users/{user_id}")
async def user_delete(
    user_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    await delete_user(db, user_id)
    return {"detail": "Пользователь удалён"}
