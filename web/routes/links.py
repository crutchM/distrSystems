from fastapi import APIRouter
from models.link import DataLink
from models.link import Link
from fastapi import Depends
from deps import get_db
import repos.links_repo as repo

from routes.middleware import throw_not_found

router = APIRouter(prefix="/links")


@router.post('/', response_model=DataLink)
def create_link(link: Link, db=Depends(get_db)):
    """Создание ссылок"""
    print(link)
    res = repo.create_link(db, link.url)
    return DataLink(id=res.id, url=res.url)


@router.get('/', response_model=DataLink)
def get_link(id: int, db=Depends(get_db)):
    """Получение ссылки"""
    res = repo.get_link(db, id)
    throw_not_found(res)
    return DataLink(id=res.id, url=res.url)

