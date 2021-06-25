from app import db
from app.models import User

u = User(username='admin',email='admin@admin.com')
db.session.add(u)
db.session.commit()

u = User.query.all()[0]
u.set_password('123')

db.session.add(u)
db.session.commit()
