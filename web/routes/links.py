import json

from fastapi import APIRouter
from models.link import DataLink
from models.link import Link
from models.link import LinkWithStatus
from fastapi import Depends
from deps import get_db
import repos.links_repo as repo
from core.rabbit import session
from routes.middleware import throw_not_found

router = APIRouter(prefix="/links")


@router.post('/', response_model=DataLink)
def create_link(link: Link, db=Depends(get_db)):
    """Создание ссылок"""
    print(link)
    res = repo.create_link(db, link.url)
    session.publish(json.dumps(res.serialize()))
    return DataLink(id=res.id, url=res.url)


@router.get('/', response_model=DataLink)
def get_link(id: int, db=Depends(get_db)):
    """Получение ссылки"""
    res = repo.get_link(db, id)
    throw_not_found(res)
    return DataLink(id=res.id, url=res.url, status=res.status)


@router.put('/', response_model=DataLink)
def update_status(link: LinkWithStatus, db=Depends(get_db)):
    """Обновление статуса"""
    res = repo.update_status(db=db, id=link.id, status=link.status)
    throw_not_found(res)
    return DataLink(id=res.id, url=res.url, status=res.status)