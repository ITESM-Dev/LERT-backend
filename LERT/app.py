import json
import os
import secrets
import time
from argon2 import PasswordHasher
from flask import jsonify, Flask
import flask
from flask_login import LoginManager
from sqlalchemy.orm import Session
from sqlalchemy import *
from LERT.db import database, session
from LERT.ica.views import ica
from LERT.opmanager.views import opManager
from LERT.manager.views import manager
from LERT.expenseType.views import expenseType
from LERT.hourType.views import hourType
from LERT.bandType.views import bandType
from LERT.user.models import User
from LERT.user.views import user
from LERT.administrator.views import admin
from LERT.icaAdmin.views import icaAdmin
from LERT.resource.views import resource
from LERT.expense.views import expense
from LERT.resourceExpense.views import resourceExpense
from LERT.db.database import connection
from db2_Connection import Db2Connection
import sys

app = Flask(__name__, static_url_path='')

def create_app():

    if os.getenv('ENVIRONMENT') == 'dev':
        app.config.from_object('config.DevelopmentConfig')
        print(os.getenv('ENVIRONMENT'))
    elif os.getenv('ENVIRONMENT') == 'prod':
        app.config.from_object('config.DevelopmentConfig')
        print(os.getenv('ENVIRONMENT'))
        database
        session

app.register_blueprint(user)
app.register_blueprint(admin)
app.register_blueprint(icaAdmin)
app.register_blueprint(resource)
app.register_blueprint(expense)
app.register_blueprint(resourceExpense)
app.register_blueprint(ica)
app.register_blueprint(opManager)
app.register_blueprint(manager)
app.register_blueprint(expenseType)
app.register_blueprint(hourType)
app.register_blueprint(bandType)

#sentence = "SELECT * FROM OOLONG"
#rows = connection.get_all(sentence)
#print(rows)
#connection._create_connection_sqlAlchemy()

# @app.route("/")
# def hello():
#     return "<h1 style='color:blue'>Hello There!</h1>"

# @app.route("/user")
# def get_user():
#     Dictionary ={'id':'eduCBA' , 'user_name':'Premium' , 'user_last_name':'2709 days'}
#     return jsonify(Dictionary)


login_manager = LoginManager()
login_manager.init_app(app)

VIDA_TOKEN = 1000 * 60 * 3

session2 = Session(connection.e)



@login_manager.user_loader
def load_user(user_id):  
    user = session2.query(User).get(user_id)

    if user == None:
        return

    return user
"""
@login_manager.request_loader
def request_loader():
    ph = PasswordHasher()

    userToken = flask.request.headers.get('token')
    tokenDB = userDB.token

    try:
        ph.verify(userToken, tokenDB)

    except Exception as e:
        print(e)
        return


    currentTimestamp = time.time()

    if(userDB.expiration + VIDA_TOKEN < currentTimestamp):
        pass
"""

@app.route('/login', methods=['POST'])
def login():

    try:
        userMail = flask.request.form['mail']
        userDBQuery = session2.query(User).filter_by(mail = userMail)
        userDB = userDBQuery.first()
        userMail = userDB.mail
    except Exception as e:
        return "Email is not valid", 401 

    ph = PasswordHasher()

    try:
        userPassword = flask.request.form['password']
        passwordDB = userDB.password 
        ph.verify(passwordDB, userPassword)
    except:
        return "Password is not valid", 401 

    token = secrets.token_urlsafe(32)
    expiration = time.time()

    userDBQuery.\
        update({User.token: ph.hash(token)}, synchronize_session='fetch')
    
    userDBQuery.\
        update({User.expiration: expiration}, synchronize_session='fetch')

    session2.commit()    

    return "Valid credentials", 200

session2.close()

if __name__ == "__main__":
    create_app().run()