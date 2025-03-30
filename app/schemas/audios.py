from pydantic import BaseModel


class Audio(BaseModel):
    id: int
    file_name: str
    file_path: str
    owner_id: int
