from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.blog import Blog
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.blog_article import ArticleCreate, ArticleUpdate
from app.schemas.blog import BlogCreate, BlogUpdate
from app.models.blog_article import BlogArticle
from app.models.tag import Tag, article_to_tag



class CRUDBlog(CRUDBase[Blog, BlogCreate, BlogUpdate]):
    def update(
        self, db: Session, *, db_obj: Blog, obj_in: Union[BlogUpdate, Dict[str, Any]]
    ) -> Blog:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_all_articles(
        self, db: Session, *, id: int, skip: int = 0, limit: int = 100
    ) -> List[BlogArticle]:
        return (
            db.query(BlogArticle)
            .filter(BlogArticle.blog_id == id, BlogArticle.status == "published")
            .order_by(BlogArticle.id)
            .offset(skip)
            .limit(limit)
            .all()
        ) 


    def search(
        self, db: Session, *, tags: List[str], skip: int = 0, limit: int = 100, user_id: Optional[int] = None
    ) -> List[BlogArticle]:
        query = (
            db.query(BlogArticle)
            .join(article_to_tag)
            .join(Tag)
            .filter(Tag.text.in_(tags))
            )
        if user_id is not None:    
            query = query.join(Blog).filter(Blog.user_id==user_id)
        query = query.order_by(BlogArticle.id).offset(skip).limit(limit)
        return query.distinct().all()

blog = CRUDBlog(Blog)        