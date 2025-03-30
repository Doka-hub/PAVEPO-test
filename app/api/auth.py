from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, crud
from app.config.database import get_db_session
from app.services.auth import get_current_user, create_access_token
from app.services.yandex_auth import get_yandex_auth_url, exchange_code_for_user_info

router = APIRouter()


@router.get("/auth/yandex")
async def yandex_auth():
    auth_url = get_yandex_auth_url()
    return {"auth_url": auth_url}


@router.get("/auth/yandex-callback")
async def yandex_callback(code: str, db: AsyncSession = Depends(get_db_session)):
    yandex_user = await exchange_code_for_user_info(code)
    user = await crud.get_user_by_yandex_id(db, yandex_user.get("id"))
    if not user:
        user = await crud.create_user(db, yandex_user)
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/auth/refresh")
async def refresh_token(current_user: schemas.User = Depends(get_current_user)):
    new_token = create_access_token({"sub": str(current_user.id)})
    return {"access_token": new_token, "token_type": "bearer"}
