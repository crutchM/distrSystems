from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    status = Column(String)

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}