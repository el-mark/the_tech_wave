from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    posts = [
        {
            'title': 'Beautiful day in Portland!'
        },
        {
            'title': 'The Avengers movie was so cool!'
        },
        {
            'title': 'This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.'
        },
        {
            'title': 'Instagram Implementa Restricciones para Proteger a Adolescentes en la Plataforma'
        },
        {
            'title': 'Apple lanza el Watch Series 10 con detección de apnea de sueño y profundidad de agua, y el iPhone 16 se lanza sin su funcionalidad más esperada de IA'
        }

    ]
    return render_template('index.html', title='Home', posts=posts)
