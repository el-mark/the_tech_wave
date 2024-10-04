from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import date 

class Article(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(510), unique=True)
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    image_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(510))
    source_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    created_at: so.Mapped[date] = so.mapped_column(sa.Date, default=date.today)

    def __repr__(self):
        return '<Article {}: {}>'.format(self.id, self.title)
