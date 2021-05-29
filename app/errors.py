# Flask mechanism for an application to install its own error pages
# creating custom error pages for the HTTP errors
from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def not_found_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
