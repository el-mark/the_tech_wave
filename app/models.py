from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Article(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(
        sa.String(64), unique=True
    )
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    image_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    views: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)

    def __repr__(self):
        return '<Article {}>'.format(self.title)