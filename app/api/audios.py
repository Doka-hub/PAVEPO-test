import os

from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db_session
from app.services import get_current_user
from app.crud import create_audio_file_record, get_audio_files_by_user
from app import schemas

router = APIRouter()

ALLOWED_AUDIO_TYPES = [
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/ogg",
    "audio/flac",
]


@router.post("/audios/upload")
async def audio_upload(
    file: UploadFile = File(...),
    file_name: str = None,
    current_user: schemas.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный тип файла. Ожидается аудио-файл."
        )

    original_filename = file.filename
    _, ext = os.path.splitext(original_filename)
    if file_name:
        base_name, provided_ext = os.path.splitext(file_name)
        if not provided_ext and ext:
            file_name = file_name + ext
    else:
        file_name = original_filename

    upload_dir = os.path.join("uploads", str(current_user.id))
    os.makedirs(upload_dir, exist_ok=True)

    base_name, ext = os.path.splitext(file_name)
    unique_file_name = file_name
    file_location = os.path.join(upload_dir, unique_file_name)

    counter = 1
    while os.path.exists(file_location):
        unique_file_name = f"{base_name}_{counter}{ext}"
        file_location = os.path.join(upload_dir, unique_file_name)
        counter += 1

    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    await create_audio_file_record(db, current_user.id, unique_file_name, file_location)
    return {"detail": "Файл загружен", "file_path": file_location}


@router.get("/audio-files", response_model=list[schemas.Audio])
async def list_audio_files(
    current_user: schemas.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    files = await get_audio_files_by_user(db, current_user.id)
    return files
