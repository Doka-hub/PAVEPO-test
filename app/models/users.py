from sqlalchemy import Column, Integer, String, Boolean
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

