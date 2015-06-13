import flask
# from flask.ext.admin import Admin, BaseView, expose, AdminIndexView, helpers
# from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy
# from wtforms.ext.sqlalchemy.orm import model_form
from flask import render_template, request, url_for, redirect, flash
# import datetime
import json
from pprint import pprint as pp

app = flask.Flask(__name__, static_folder='./public_folder', static_url_path='')

app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/dan/University/projects/trust/database.db'


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

    pp(request.form)
    #form = user_form(request.form)
    # user = User(form.username.data, form.email.data,
    #             form.password.data, form.github_url.data)
    # db.session.add(user)
    # db.session.commit()
    # flash('Thanks for registering')
    # login_user(user)
    return "hello" #redirect(url_for('user_view', user_id=user.id))

    return render_template('user_register_view.html', form=form)


@app.route("/test")
def test():
    return json.dumps([1, 2, 3])


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')