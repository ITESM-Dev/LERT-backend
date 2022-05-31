from crypt import methods
from flask import Blueprint
from flask_login import login_required
from LERT.authorization.roles import admin_permission
#from LERT.db.session import session
from LERT.db.database import connection
from sqlalchemy.orm import Session
from LERT.user.models import User
from LERT.administrator.models import Administrator
from LERT.opmanager.models import OpManager
from LERT.resource.models import Resource
from LERT.manager.models import Manager
from LERT.icaAdmin.models import ICAAdmin
import flask
from argon2 import PasswordHasher

user = Blueprint('user', __name__)

@user.route("/")
def hello():
    return "hello"

@user.route("/name")
@admin_permission.require(http_exception=403)
@login_required
def name():
    return "ricardo"

@user.route("/signUp", methods=['POST', 'GET'])
def createUser():
    ph = PasswordHasher()

    statusCode = flask.Response(status=201)
    userName = flask.request.form['name']
    userMail = flask.request.form['mail']
    userPassword = ph.hash(flask.request.form['password'])
    userRole = flask.request.form['role']
    userCountry = flask.request.form['country']
    
    try:
        session = Session(connection.e)

        user1 = User(name = userName, mail = userMail, password = userPassword, role = userRole, country = userCountry)
        session.add(user1)
        session.commit() 
        
    except Exception as e:
        return "Email already exists", 401

    userDB = session.query(User).filter_by(mail = userMail).first()

    if (userRole == "Admin"):
        admin = Administrator(idUser = userDB.idUser)
        session.add(admin)
        session.commit()
    elif (userRole == "IcaAdmin"):
        icaAdmin = ICAAdmin(idUser = userDB.idUser)
        session.add(icaAdmin)
        session.commit()
    elif (userRole == "OpManager"):
        opManager = OpManager(idUser = userDB.idUser, status = "Active")
        session.add(opManager)
        session.commit()
    elif (userRole == "Manager"):    
        manager = Manager(idUser = userDB.idUser, recoveryStatus = "Not completed")
        session.add(manager)
        session.commit()
    else:
        resource = Resource(idUser = userDB.idUser)
        session.add(resource)
        session.commit()
    session.close()


    return statusCode