from pydantic import BaseModel


class User(BaseModel):
    id: int
    yandex_id: str
    email: str | None
    full_name: str | None
    is_superuser: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: str | None
    full_name: str | None
