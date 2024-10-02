from flask import render_template
from app import app
from app.posts import posts  # Import the posts variable

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', posts=posts)


@app.route('/article/<int:id>')
def article(id):
    # # Fetch the article from the database using the id
    # post = Post.query.get_or_404(id)
    
    # # Increment the view count
    # post.views += 1
    # db.session.commit()
    # Select the post based on the id
    if 1 <= id <= len(posts):
        post = posts[id - 1]
    else:
        # Handle case where id is out of range
        post = {'title': 'Article not found'}
    
    return render_template('article.html', title=post['title'], post=post, posts=posts)

