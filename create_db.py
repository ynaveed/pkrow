from main import app
from main import db, User, Transaction

db.drop_all()
db.create_all()

new_user = User(username='Daniil Pakhomov', email='warmspringwinds@gmail.com',
                password='123', stars=5)

new_user_2 = User(username='Areeb', email='areeb@gmail.com', password='100', stars=4)

new_transaction = Transaction(paymill_id='tran_e6a03da2f67eb54c3e9cd45f4c7f',
                              amount=4200,
                              currency='EUR',
                              user_id=1,
                              receiver_id=2)


db.session.add(new_user)
db.session.add(new_user_2)
db.session.add(new_transaction)
db.session.commit()