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
    views: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)

    def __repr__(self):
        return '<Article {}: {}>'.format(self.id, self.title)

    def formatted_date(self):
        month_translations = {
            'January': 'enero', 'February': 'febrero', 'March': 'marzo',
            'April': 'abril', 'May': 'mayo', 'June': 'junio',
            'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
            'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
        }
        # date_with_format = self.created_at.strftime('%d de %B de %Y')
        date_with_format = self.created_at.strftime('%d de %B')
        for eng, esp in month_translations.items():
            date_with_format = date_with_format.replace(eng, esp)
        return date_with_format
