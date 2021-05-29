from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, DeepSpeechLog

class UserModelCase(unittest.TestCase):
    # executes befor and after each test respectively
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    # executes befor and after each test respectively
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cow')
        self.assertFalse(u.check_password('frog'))
        self.assertTrue(u.check_password('cow'))

class DeepSpeechLogModelCase(unittest.TestCase):
    # executes befor and after each test respectively
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    # executes befor and after each test respectively
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_deepspeechlog(self):
        now = datetime.utcnow()
        dsl = DeepSpeechLog(body="first test", timestamp=now + timedelta(seconds=1))
        db.session.add(dsl)
        db.session.commit()


if __name__ == '__main__':
    unittest.main(verbosity=2)