from sqlalchemy.orm import Session
from core.db.models import Link


def create_link(db: Session, url: str) -> Link:
    link = Link(url=url)
    db.add(link)
    db.commit()
    return link


def get_link(db: Session, id: int) -> Link:
    return db.query(Link).filter(Link.id == id).one_or_none()



def update_status(db: Session, id: int, status: str) -> Link:
    link: Link = db.query(Link) \
        .filter(Link.id == id) \
        .one_or_none()
    if link is None:
        return None
    link.status = status
    db.commit()

    return link


