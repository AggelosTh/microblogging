from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base


article_to_tag = Table(
    "article_to_tag",
    Base.metadata,
    Column("tag_id", ForeignKey("tag.id")),
    Column("blog_article_id", ForeignKey("blog_article.id"))
)


class Tag(Base):
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    articles = relationship("BlogArticle", secondary=article_to_tag)
