from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from flask_migrate import current
from werkzeug.wrappers import request
from werkzeug.urls import url_parse
from flask.helpers import url_for
from flask import render_template, flash, redirect, request
from app.models import User
from app.forms import LoginForm, EditProfileForm
from app import app, db

@app.route('/')
@app.route('/index')
@login_required         # decorator, only logged useres can visit the above routes
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


@app.route('/user/<username>')      # route has a dynamic component in it
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


# Decorator function, executed right befor the view function.
@app.before_request
def before_request():
    if current_user.is_authenticated:                   # if the user is logged in, than set the last_seen fielt to curent time
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# View function
@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():                       # if validation is true copy the data form into the user object and then write it to the database
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':                       # request by the first time
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)