from cgitb import text
from datetime import datetime
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.blog import Blog
from app.models.user import User
from app.models.blog_article import BlogArticle
from app.models.tag import Tag
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.blog_article import Article, ArticleCreate, ArticleUpdate
from app.core.celery_app import celery_app

class CRUDArticle(CRUDBase[BlogArticle, ArticleCreate, ArticleUpdate]):
    # def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
    #     return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, owner_id: int, obj_in: ArticleCreate) -> BlogArticle:
        blog = db.query(Blog).filter(Blog.user_id==owner_id).first()
        db_obj = BlogArticle(
            blog_id=blog.id,
            title=obj_in.title,
            body=obj_in.body,
        )
        for tag in obj_in.tags:
            db_tag = db.query(Tag).filter(Tag.text == tag).first()
            if db_tag is None:
                db_tag = Tag(text=tag)
            db_obj.tags.append(db_tag)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: BlogArticle, obj_in: Union[ArticleUpdate, Dict[str, Any]]
    ) -> BlogArticle:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        print(obj_in)
        if update_data.get("tags") is not None:
            db_obj.tags.clear()
            for tag in update_data.get("tags"):
                db_tag = db.query(Tag).filter(Tag.text == tag).first()
                if db_tag is None:
                    db_tag = Tag(text=tag)
                db_obj.tags.append(db_tag)
            del update_data["tags"]
        return super().update(db, db_obj=db_obj, obj_in=update_data)


    def status(self, blog: BlogArticle) -> str:
        return blog.status

    def publish(self, db: Session, *, article: BlogArticle, publication_date=Optional[datetime]):
        if publication_date is None:
            status = "published"
            publication_date = datetime.now()
        else:
            status = "pre-published"
        article.status = status
        article.publication_date = publication_date
        db.add(article)
        db.commit()
        db.refresh(article)
        return article    

article = CRUDArticle(BlogArticle)
