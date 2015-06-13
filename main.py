import flask
# from flask.ext.admin import Admin, BaseView, expose, AdminIndexView, helpers
# from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy
# from wtforms.ext.sqlalchemy.orm import model_form
from flask import render_template, request, url_for, redirect, flash
# import datetime
import json
from pprint import pprint as pp
import paymill

app = flask.Flask(__name__, static_folder='./public_folder', static_url_path='')

app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/dan/University/projects/trust/database.db'

PRIVATE_KEY = 'db0957a0c5ce4fb9189c3110af58cd03'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    #projects = db.relationship("ProjectProposal", backref="author")
    
    def __init__(self, username="", email="", password=""):
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self):
        return '<User %r>' % self.username

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paymill_id = db.Column(db.String(120))
    amount = db.Column(db.Integer)
    currency = db.Column(db.String(120))
    user_id = db.Column(db.Integer)

    def __init__(self, paymill_id, amount, currency, user_id=1):
        self.paymill_id = paymill_id
        self.amount = amount
        self.currency = currency
        self.user_id = user_id

    def __repr__(self):
        return '<Transaction %r>' % self.paymill_id


@app.route("/user/<int:user_id>")
def user_view(user_id):
    
    user = User.query.get_or_404(user_id)
    
    return render_template('user_view.html', user=user)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/pay")
def pay_first_stage():
    return render_template('paymill.html')

@app.route("/user", methods=['POST'])
def user_transaction():

    # Everything works only for one user for demosntration.

    token = request.form.get('token')
    amount = request.form.get('amount')
    currency = request.form.get('currency')
    context = paymill.PaymillContext(PRIVATE_KEY)
    transaction = context.transaction_service.create_with_token(token=token,
                                                                amount=amount,
                                                                currency=currency,
                                                                description='test')
    if transaction.status == 'closed':
        print transaction.id
        new_transaction = Transaction(paymill_id=transaction.id,
                                      amount=amount,
                                      currency=currency,
                                      user_id=1)

        db.session.add(new_transaction)
        db.session.commit()
        return json.dumps({'status': '200 ok'})

    return json.dumps({'status': '500'})


@app.route("/test")
def test():
    return json.dumps([1, 2, 3])


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')