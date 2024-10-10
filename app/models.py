from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import date 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Article(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(510), unique=True)
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    image_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    source: so.Mapped[Optional[str]] = so.mapped_column(sa.String(510))
    source_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    created_at: so.Mapped[date] = so.mapped_column(sa.Date, default=date.today)
    views: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    comments = so.relationship('Comment', back_populates='article')

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

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(150), unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(150), unique=True, nullable=False)
    lastname: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=True) 
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    is_admin: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=False)
    comments = so.relationship('Comment', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def is_active(self):
        # Return True if the user is active, otherwise False
        return True  # or some condition to check if the user is active

class Comment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    created_at: so.Mapped[date] = so.mapped_column(sa.DateTime, default=sa.func.now())
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    article_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('article.id'), nullable=False)

    user = so.relationship('User', back_populates='comments')
    article = so.relationship('Article', back_populates='comments')

    def __repr__(self):
        return '<Comment {} by User {} on Article {}>'.format(self.id, self.user_id, self.article_id)
