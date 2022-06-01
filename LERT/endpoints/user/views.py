from crypt import methods
from flask import Blueprint
from flask_login import login_required
from LERT.endpoints.authorization.roles import admin_permission
#from LERT.db.session import session
from LERT.db.database import connection
from sqlalchemy.orm import Session
from LERT.endpoints.user.models import User
from LERT.endpoints.administrator.models import Administrator
from LERT.endpoints.opmanager.models import OpManager
from LERT.endpoints.resource.models import Resource
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.icaAdmin.models import ICAAdmin
import flask
from argon2 import PasswordHasher

user = Blueprint('user', __name__)

@user.route("/signUp", methods=['POST', 'GET'])
def createUser():
    ph = PasswordHasher()

    statusCode = flask.Response(status=201)
    userName = flask.request.json['name']
    userMail = flask.request.json['mail']
    userPassword = ph.hash(flask.request.json['password'])
    userBand = int(flask.request.json['band'])
    userRole = flask.request.json['role']
    userCountry = flask.request.json['country']
    
    try:
        session = Session(connection.e)

        user1 = User(name = userName, mail = userMail, password = userPassword, band = userBand, role = userRole, country = userCountry)
        session.add(user1)
        session.commit() 
        
    except Exception as e:
        print(e)

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