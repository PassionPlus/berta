from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Admin'}
    deepspeechlogs = [
        {
            'date': '25.05.2020',
            'body': 'Turn on lights'
        },
        {
            'date': '26.05.2020',
            'body': 'Tell joke'
        }    
    ]
    return render_template('index.html', title='Home', user=user, deepspeechlogs=deepspeechlogs)