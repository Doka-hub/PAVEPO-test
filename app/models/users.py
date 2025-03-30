from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    yandex_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    is_superuser = Column(Boolean, default=False)
    audio_files = relationship("AudioFile", back_populates="owner")


class AudioFile(Base):
    __tablename__ = "audio_files"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_name = Column(String)
    file_path = Column(String)
    owner = relationship("User", back_populates="audio_files")
