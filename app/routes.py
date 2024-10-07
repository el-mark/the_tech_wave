from flask import render_template, request, redirect
from app import app
from app.models import Article  # Import Article from models

# @app.before_request
# def enforce_https():
#     if request.headers.get('X-Forwarded-Proto', 'http') == 'http':
#         return redirect(request.url.replace('http://', 'https://'))

@app.route('/')
@app.route('/index')
def index():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('index.html', articles=articles)

@app.route('/article/<int:id>')
def article(id):
    # Fetch the article from the database using the id
    article = Article.query.get_or_404(id)
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('article.html', title=article.title, article=article, articles=articles)

@app.route('/articles')
def articles():
    articles = Article.query.all()
    return '<br>'.join([article.title for article in articles])
