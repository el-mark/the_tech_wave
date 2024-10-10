from flask import render_template, request, redirect, make_response, flash, url_for
from app import app, db
from app.models import Article, User  # Import Article and User from models
from flask_login import login_user, logout_user, login_required, current_user

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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('signup'))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Signup successful!')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        flash('Login successful!')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/user')
@login_required
def user():
    return {'email': current_user.email, 'id': current_user.id}
