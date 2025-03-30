from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db_session
from .services import get_tron_info

router = APIRouter()


@router.post("/info", response_model=TronInfoResponse)
async def get_info(
    address: TronAddress,
    db: AsyncSession = Depends(get_db_session),
):
    tron_info = await get_tron_info(address.address)

    instance = RequestLog(address=address.address)
    db.add(instance)

    await db.commit()

    return tron_info
