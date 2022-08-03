from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.tag import article_to_tag


class BlogArticle(Base):
    __tablename__ = "blog_article"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    status = Column(String, index=True)
    publication_date = Column(DateTime)
    blog_id = Column(Integer, ForeignKey("blog.id"))
    blog = relationship("Blog", back_populates="blog_articles")
    tags = relationship("Tag", secondary=article_to_tag) 
