from flask import render_template, request, redirect, make_response
from app import app, db
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
    
    # Check if the user has already viewed this article
    viewed = request.cookies.get(f'viewed_{id}')
    
    if not viewed:
        # Increment the view count
        article.views += 1
        db.session.commit()
    
    # Get other articles for the "More news" section
    articles = Article.query.order_by(Article.created_at.desc()).all()
    
    # Prepare the response
    response = make_response(render_template('article.html', title=article.title, article=article, articles=articles))
    
    if not viewed:
        # Set a cookie to mark this article as viewed by this user
        response.set_cookie(f'viewed_{id}', 'true', max_age=86400)  # Cookie expires in 24 hours
    
    return response

@app.route('/articles')
def articles():
    articles = Article.query.all()
    return '<br>'.join([article.title for article in articles])
