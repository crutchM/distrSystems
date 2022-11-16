from typing import Optional

from pydantic import BaseModel


class Link(BaseModel):
    url: str


class LinkWithStatus(BaseModel):
    id: int
    status: str

class DataLink(Link):
    id: int
    status: Optional[str]

    class Config:
        orm_mode=True