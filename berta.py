# python top-level script that defines the Flask application instance
from app import app, db
from app.models import User, DeepSpeechLog

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'DeepSpeechLog': DeepSpeechLog}
