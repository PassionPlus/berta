from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.wrappers import request
from werkzeug.urls import url_parse
from flask.helpers import url_for
from flask import render_template, flash, redirect, request
from app.models import User
from app.forms import LoginForm
from app import app

@app.route('/')
@app.route('/index')
@login_required         # only logged useres can visit the above routes
def index():
    deepspeechlogs = [{
            'timestamp': '25',
            'body': 'text'
        },
        {
        'timestamp': '24',
        'body': 'anderere text'
        }
    ]
     
    return render_template('index.html', title='Home', deepspeechlogs=deepspeechlogs)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()        # give me the first database entry with the usersername from the form
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)        # user is registerd and can navigate
        next_page = request.args.get('next')                    # all information that the client sent with the request in dict format 
        # if the login URL does not have a next argument, then the user is redirected to the index page
        # if the login URL includes a next argument that is set to a relative path (or in other words, a URL without the domain portion), then the user is redirected to that URL
        # if the login URL includes a next argument that is set to a full URL that includes a domain name, then the user is redirected to the index page
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)                              
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))