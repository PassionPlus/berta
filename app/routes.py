from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from flask_migrate import current
from werkzeug.wrappers import request
from werkzeug.urls import url_parse
from flask.helpers import url_for
from flask import render_template, flash, redirect, request
from app.models import User, DeepSpeechLog
from app.forms import DeepSpeechLogForm, LoginForm, EditProfileForm
from app import app, db, berta

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required         # decorator, only logged useres can visit the above routes
def index():
    form = DeepSpeechLogForm()
    
    if form.validate_on_submit():
        #deepspeechlog = DeepSpeechLog(question=form.deepspeechlog.data) # inserts a new Log record into the database
        _question = form.deepspeechlog.data
        _answer = berta.test_phrase(_question)
        deepspeechlog = DeepSpeechLog(question=_question, answer = _answer)
        db.session.add(deepspeechlog)
        db.session.commit()
        flash('Your deepspeechlog is now live!')
        return redirect(url_for('index'))       # standart practice to response to POST request, for refresh (Post/redirect/Get pattern)
    page = request.args.get('page', 1, type=int)
    deepspeechlogs = DeepSpeechLog.query.order_by(DeepSpeechLog.timestamp.desc()).paginate(                 # gets all DeepSpeechlogs by order paginated
        page, app.config['POSTS_PER_PAGE'], False)
        # from Pagination object attribute next_num: page number for the next page
    next_url = url_for('index', page=deepspeechlogs.next_num) \
        if deepspeechlogs.has_next else None                    # from Pagination object attribute has_next: true if there is at least one ore page after the current one
        # from Pagination object attribute prev_num: page number for the previous page
    prev_url = url_for('index', page=deepspeechlogs.prev_num) \
        if deepspeechlogs.has_prev else None                    # from Pagination object attribute has_prev: true if there is at least one more page before the current one
    return render_template('index.html', title='Home', form=form, deepspeechlogs=deepspeechlogs.items, next_url=next_url, prev_url=prev_url)        # items attribute from Pagination class from Flask-SQLAlchemy, contains the list of items retrieved for the selected page 

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

@app.route('/plugin')      # route has a dynamic component in it
@login_required
def plugin():
    return render_template('plugin.html', user=None)

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
    form = EditProfileForm(current_user.username)       # to use validation method add orignial username argument, to prevent duplicats
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
