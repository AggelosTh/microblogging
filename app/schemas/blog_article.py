from datetime import datetime
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Query
import markdown2

from pydantic import BaseModel, validator

class ArticleBase(BaseModel):
    title: str
    body: str

# Properties to receive via API on creation
class ArticleCreate(ArticleBase):
    tags: List[str]
    # password: str


# Properties to receive via API on update
class ArticleUpdate(ArticleBase):
    # password: Optional[str] = None
    tags: Optional[List[str]] = None

class ArticleInDBBase(ArticleBase):
    id: Optional[int] = None
    blog_id: Optional[int] = None
    status: Optional[str] = None
    publication_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class Tag(BaseModel):
    text: str
    class Config:
        orm_mode = True

# # Additional properties to return via API
class Article(ArticleInDBBase):
    tags: List[Tag]
    @validator("*", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v

    @validator("body")
    def body_to_html(cls, v):
        return markdown2.markdown(v)    


# # Additional properties stored in DB
class ArticleInDB(ArticleInDBBase):
    pass

    # hashed_password: str