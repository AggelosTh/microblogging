from datetime import datetime
from typing import Any, List, Optional
from urllib import response

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

router = APIRouter()


@router.get('/blog/{id}', response_model=List[schemas.Article])
def read_blog(
    id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit : int = 100,
) -> Any:
    """
    Retrieve blog.
    """
    blog = crud.blog.get_all_articles(db, id=id, skip=skip, limit=limit)
    return blog 


@router.put("/{id}", response_model=schemas.Article)
def update_article(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    article_in: schemas.ArticleUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    article = crud.article.get(db=db, id=id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if not crud.user.is_superuser(current_user) and (article.blog.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    article = crud.article.update(db=db, db_obj=article, obj_in=article_in)
    return article


@router.post("/", response_model=schemas.Article)
def create_article(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ArticleCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new article.
    """
    article = crud.article.create(db=db, obj_in=item_in, owner_id=current_user.id)
    return article


@router.post("/publish/{id}", response_model=schemas.Article)
def publish_article(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    publication_date: Optional[datetime] = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    article = crud.article.get(db=db, id=id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if not crud.user.is_superuser(current_user) and (article.blog.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    return crud.article.publish(db=db, article=article, publication_date=publication_date)


@router.get('/blog/search/', response_model=List[schemas.Article])
def search_blog(
    tags: str,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit : int = 100,
) -> Any:
    """
    Search articles by tags.
    """
    tags = [tag.strip() for tag in tags.split(',')]
    return crud.blog.search(db, tags=tags, skip=skip, limit=limit)


@router.get('/blog/{user_id}/search/', response_model=List[schemas.Article])
def search_blog_by_user(
    tags: str,
    user_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit : int = 100,
) -> Any:
    """
    Search articles by author.
    """
    tags = [tag.strip() for tag in tags.split(',')]
    return crud.blog.search(db, user_id=user_id, tags=tags, skip=skip, limit=limit)