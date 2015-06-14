import flask
# from flask.ext.admin import Admin, BaseView, expose, AdminIndexView, helpers
# from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy
# from wtforms.ext.sqlalchemy.orm import model_form
from flask import render_template, request, url_for, redirect, flash, jsonify
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
    stars = db.Column(db.Integer)

    def __init__(self, username="", email="", password="", stars=5):
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
    receiver_id = db.Column(db.Integer)

    def __init__(self, paymill_id, amount, currency, user_id=1, receiver_id=2):
        self.paymill_id = paymill_id
        self.amount = amount
        self.currency = currency
        self.user_id = user_id
        self.receiver_id = receiver_id

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'         : self.id,
           'paymill_id': self.paymill_id,
           'amount': self.amount,
           'currency': self.currency,
           'author_id': self.user_id,
           'receiver_id': self.receiver_id
       }

    def __repr__(self):
        return '<Transaction %r>' % self.paymill_id


@app.route("/user/<int:user_id>")
def user_view(user_id):
    
    user = User.query.get_or_404(user_id)
    
    return render_template('user_view.html', user=user)

@app.route("/pay_receiver")
def index():
    return render_template('pay_receiver.html')

@app.route("/pay_bank_details", methods=['POST', 'GET'])
def pay_first_stage():

    amount = request.form.get('amount')
    escrow_days = request.form.get('escrow_days')

    return render_template('pay_bank_details.html',
                           amount=amount,
                           escrow_days=escrow_days)

@app.route("/transaction_run", methods=['POST'])
def pay_second_stage():

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
        flash('Transaction was successful. Going to transaction page.')
        return redirect(url_for('view_transactions'))

    flash("Transaction wasn't successful. Try once again")
    return redirect(url_for('pay_first_stage'))

@app.route("/transactions_view")
def view_transactions():

    receiver = User.query.filter_by(id=2).first()
    transactions = Transaction.query.all()
    return render_template('transactions_view.html',
                           transactions=transactions,
                           receiver=receiver)

@app.route("/manage/<int:transaction_id>/")
def manage_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    return render_template('manage_transaction.html',
                           transaction=transaction)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')