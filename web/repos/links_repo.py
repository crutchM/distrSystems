from sqlalchemy.orm import Session
from core.db.models import Link


def create_link(db: Session, url: str) -> Link:
    link = Link(url=url)
    db.add(link)
    db.commit()
    return link


def get_link(db: Session, id: int) -> Link:
    return db.query(Link).filter(Link.id == id).one_or_none()


