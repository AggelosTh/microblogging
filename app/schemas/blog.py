from typing import Optional, List

from pydantic import BaseModel, EmailStr


# Shared properties
class BlogBase(BaseModel):
    articles: List[str]

class BlogCreate(BlogBase):
    password: str

class BlogUpdate(BlogBase):
    articles: List[str]


class BlogInDBBase(BlogBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Blog(BlogInDBBase):
    pass    


class BlogInDB(BlogInDBBase):
    pass