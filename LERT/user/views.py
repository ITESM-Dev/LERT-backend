from crypt import methods
from flask import Blueprint
#from LERT.db.session import session
from LERT.db.database import connection
from sqlalchemy.orm import Session
from LERT.user.models import User
import flask
from argon2 import PasswordHasher

user = Blueprint('user', __name__)

@user.route("/")
def hello():
    return "hello"

@user.route("/name")
def name():
    return "ricardo"

@user.route("/signUp", methods=['POST', 'GET'])
def createUser():
    ph = PasswordHasher()

    statusCode = flask.Response(status=201)
    userName = flask.request.form['name']
    userMail = flask.request.form['mail']
    userPassword = ph.hash(flask.request.form['password'])
    userToken = ph.hash(flask.request.form['token'])
    userExpiration = flask.request.form['expiration']
    userRole = flask.request.form['role']

    
    try:
        session = Session(connection.e)

        user1 = User(name = userName, mail = userMail, password = userPassword,
        token = userToken, expiration = userExpiration, role = userRole)
        session.add(user1)
        session.commit() 
        session.close()
        
    except Exception as e:
        print(e)

    return statusCode