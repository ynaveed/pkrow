from main import app
from main import db, User

db.drop_all()
db.create_all()

new_user = User(username='Daniil Pakhomov', email='warmspringwinds@gmail.com',
                password='123')

db.session.add(new_user)
db.session.commit()