from backend.app.app.models import blog_article
from raven import Client

from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.blog_article import BlogArticle

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task
def published_blogs(article_id: int) -> bool:
    with SessionLocal() as db:
        article = db.query(BlogArticle).filter(BlogArticle.id==article_id).first()
        article.status = "published"
        db.add(article)
        db.commit()
        return True
