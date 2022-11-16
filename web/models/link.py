from pydantic import BaseModel


class Link(BaseModel):
    url: str


class DataLink(Link):
    id: int

    class Config:
        orm_mode=True