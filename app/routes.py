from flask import render_template, request, redirect, make_response, flash, url_for, jsonify
from app import app, db
from app.models import Article, User, Comment
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from flask_googlestorage import GoogleStorage, Bucket
import os

# @app.before_request
# def enforce_https():
#     if request.headers.get('X-Forwarded-Proto', 'http') == 'http':
#         return redirect(request.url.replace('http://', 'https://'))


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        files = Bucket("files")

        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file_storage = request.files['file']
        if file_storage.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = files.save(file_storage)  # Save the file
        public_url = files.url(filename)  # Get the public URL

        return jsonify({'url': public_url}), 200
    else:
        return render_template('upload_file.html')

@app.route('/')
@app.route('/index')
def index():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('index.html', os=os, articles=articles)

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
    articles = Article.query.filter(Article.id != id).order_by(Article.created_at.desc()).all()
    
    # Prepare the response
    response = make_response(render_template('article.html', os=os, title=article.title, article=article, articles=articles))
    
    if not viewed:
        # Set a cookie to mark this article as viewed by this user
        response.set_cookie(f'viewed_{id}', 'true', max_age=86400)  # Cookie expires in 24 hours
    
    return response

@app.route('/article/<int:id>/comment', methods=['POST'])
@login_required
def post_comment(id):
    article = Article.query.get_or_404(id)
    
    # Get the comment body from the form
    body = request.form['body']
    
    # Create a new comment
    comment = Comment(
        body=body, user_id=current_user.id, article_id=article.id,
        created_at=datetime.utcnow()
    )
    
    # Add the comment to the database
    db.session.add(comment)
    db.session.commit()
    
    flash('Comment posted successfully!')
    return redirect(url_for('article', id=article.id))

@app.route('/articles')
def articles():
    articles = Article.query.all()
    return '<br>'.join([article.title for article in articles])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('signup'))
        user = User(name=name, lastname=lastname, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Signup successful!')
        return redirect(url_for('index'))
    return render_template('signup.html', os=os)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('El correo y/o la contraseña son incorrectos.')
            return redirect(url_for('login'))
        login_user(user)
        flash('Sesión iniciada!')
        return redirect(url_for('index'))
    return render_template('login.html', os=os)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente!')
    return redirect(url_for('index'))

@app.route('/user')
@login_required
def user():
    return {'email': current_user.email, 'id': current_user.id}

@app.route('/create_article', methods=['GET', 'POST'])
@login_required
def create_article():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        image_url = request.form['image_url']
        source = request.form['source']
        source_name = request.form['source_name']
        created_at = request.form['created_at']

        article = Article(
            title=title, body=body, image_url=image_url,
            source=source, source_name=source_name, created_at=created_at
        )

        db.session.add(article)
        db.session.commit()
        flash('Article created successfully!')
        return redirect(url_for('index'))
    
    return render_template('create_article.html', os=os)
