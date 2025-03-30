from pydantic import BaseModel


class User(BaseModel):
    id: int
    yandex_id: str
    email: str
    full_name: str
    is_superuser: bool
