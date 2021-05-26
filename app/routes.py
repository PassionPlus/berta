from flask.helpers import url_for
from app.forms import LoginForm
from flask import render_template, flash, redirect
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

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login request for user {}, remeber_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)