from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


async def create_audio_file_record(db: AsyncSession, user_id: int, file_name: str, file_path: str):
    audio_file = models.AudioFile(user_id=user_id, file_name=file_name, file_path=file_path)
    db.add(audio_file)
    await db.commit()
    return audio_file


async def get_audio_files_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.AudioFile).where(models.AudioFile.user_id == user_id))
    return result.scalars().all()
