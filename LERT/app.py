from multiprocessing import Manager
from LERT.db import database
from LERT.endpoints.ica.views import ica
from LERT.endpoints.opmanager.views import opManager
from LERT.endpoints.manager.views import manager
from LERT.endpoints.expenseType.views import expenseType
from LERT.endpoints.hourType.views import hourType
from LERT.endpoints.bandType.views import bandType
from LERT.endpoints.user.models import User
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.user.views import user
from LERT.endpoints.administrator.views import admin
from LERT.endpoints.icaAdmin.views import icaAdmin
from LERT.endpoints.resource.views import resource
from LERT.endpoints.expense.views import expense
from LERT.endpoints.resourceExpense.views import resourceExpense
from LERT.endpoints.currentPeriod.views import currentPeriod
from LERT.db.database import connection
import LERT.db.dbCreation
from crypt import methods
import os
import secrets
import time
from flask import Flask
import flask
import requests
from sqlalchemy.orm import Session
from sqlalchemy import *
import sys
from flask_cors import CORS, cross_origin
from argon2 import PasswordHasher
from flask_principal import *
from flask_login import LoginManager, login_required
import flask_login

app = Flask(__name__, static_url_path='')
app.secret_key = secrets.token_urlsafe(16)

CORS(app)

principals = Principal(app)
principals._init_app(app)

admin_permission = Permission(RoleNeed('Admin'))
opManager_permission = Permission(RoleNeed('OpManager'))
manager_permission = Permission(RoleNeed('Manager'))
icaAdmin_permission = Permission(RoleNeed('IcaAdmin'))
manager_or_IcaAdmin = Permission(RoleNeed('Manager'), RoleNeed('IcaAdmin'))
manager_or_OpManager = Permission(RoleNeed('Manager'), RoleNeed('OpManager'))
manager_or_OpManager_or_icaAdmin = Permission(RoleNeed('Manager'), RoleNeed('OpManager'), RoleNeed('IcaAdmin'))

def create_app():

    if os.getenv('ENVIRONMENT') == 'dev':
        app.config.from_object('config.DevelopmentConfig')
    elif os.getenv('ENVIRONMENT') == 'prod':
        app.config.from_object('config.ProductionConfig')
    database
    
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
app.register_blueprint(currentPeriod)

login_manager = LoginManager()
login_manager.init_app(app)

VIDA_TOKEN = 1000 * 60 * 3

@login_manager.user_loader
def load_user(idUser):  
    session = Session(connection.e)

    user = session.query(User).get(idUser)

    if user == None:
        return "User not found", 401
   
    session.close()
   
    return user

@login_manager.request_loader
def request_loader(request):
    
    ph = PasswordHasher()

    try:
        
        userToken = request.headers.get('token')
        userMail = request.headers.get('mail')
  
    except Exception as e:
        return "No credentials", 401

    try:
        session = connection.session
        userDBQuery = session.query(User).filter_by(mail = userMail)
        userDB = userDBQuery.first()
        userMail = userDB.mail
        session.close()
    except Exception as e:
        return "Email is not valid", 401 

    userRole = userDB.role
    tokenDB = userDB.token
    
    try:
        
        ph.verify(tokenDB, userToken)

    except:
        return "Token not valid", 401
    

    currentTimestamp = time.time()

    if(userDB.expiration + VIDA_TOKEN < currentTimestamp):
        return 


    session = connection.session

    userDBQuery.\
        update({User.expiration: currentTimestamp}, synchronize_session='fetch')

    
    result = User()
    result.id = userMail
    result.role = userRole

    identity_changed.send(current_app._get_current_object(), identity=Identity(userDB.idUser))
    
    session.close()

    return result

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):

    try:
        session = connection.session

        userDBQuery = session.query(User).filter_by(idUser = identity.id).first()

        # Add the UserNeed to the identity
        if hasattr(identity, 'id'):
            identity.provides.add(UserNeed(userDBQuery.idUser))

        # Assuming the User model has a list of roles, update the
        # identity with the roles that the user provides
        
        identity.provides.add(RoleNeed(userDBQuery.role))

        session.close()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)  
    except Exception as e:
        return e


@app.route('/login', methods=['POST'])
@cross_origin()
def login():

    try:
        session = connection.session
        userMail = flask.request.json['mail']
        userDBQuery = session.query(User).filter_by(mail = userMail)
        userDB = userDBQuery.first()
        userMail = userDB.mail
        session.close()
    except Exception as e:
        return "Email is not valid", 401 

    ph = PasswordHasher()

    try:
        userPassword = flask.request.json['password']
        passwordDB = userDB.password 
        ph.verify(passwordDB, userPassword)
    except:
        return "Password is not valid", 401 

    token = secrets.token_urlsafe(32)
    expiration = time.time()
    
    session = connection.session

    userDBQuery.\
        update({User.token: ph.hash(token)}, synchronize_session='fetch')
    
    userDBQuery.\
        update({User.expiration: expiration}, synchronize_session='fetch')

    session.commit()  

    result = {
        "id": userDB.idUser,
        "name": userDB.name,
        "mail": userDB.mail,
        "band": userDB.band,
        "role": userDB.role,
        "country": userDB.country,
        "token": token
    }
    session.close()
    return result, 200

@app.errorhandler(403)
def permission_denied(e):
    return "Forbidden", 403
    

@login_manager.unauthorized_handler
def handler():
    return 'No autorizado', 401

@app.route("/logout")
@cross_origin() 
@login_required
def logout():
    session = connection.session

    userDBQuery = session.query(User).filter_by(mail = flask_login.current_user.id)
    userDBQuery.\
        update({User.expiration: 0}, synchronize_session='fetch')

    session.close()

    return "Logged Out", 200


@app.route('/loginICAAdmin', methods=['POST'])
@cross_origin()
@icaAdmin_permission.require(http_exception=403)
def loginICAAdmin():

    try:
        session = connection.session

        userMail = flask.request.json['mailManager']
        userToken = flask.request.json['token']

        userDBQuery = session.query(User).filter_by(mail = userMail)
        userDB = userDBQuery.first()
        userMail = userDB.mail

        session.close()

    except Exception as e:
        return "Email is not valid", 401 

    try:
        session = connection.session

        userToken = flask.request.json['token']
        managerDB = session.query(Manager).filter_by(idUser = userDB.idUser).first()
        tokenDB = managerDB.tokenAuthenticator

        session.close()

        if tokenDB != userToken:
            return "Token is not valid", 401
                    
    except:
        return "Token is not valid", 401 

    token = secrets.token_urlsafe(32)
    expiration = time.time()

    ph = PasswordHasher()

    session = connection.session

    userDBQuery.\
        update({User.token: ph.hash(token)}, synchronize_session='fetch')
    
    userDBQuery.\
        update({User.expiration: expiration}, synchronize_session='fetch')

    session.commit()  

    result = {
        "id": userDB.idUser,
        "name": userDB.name,
        "mail": userDB.mail,
        "band": userDB.band,
        "role": userDB.role,
        "country": userDB.country,
        "token": token
    }

    managerDB.tokenAuthenticator = None
    session.commit()
    session.close()
    
    return result, 200



if __name__ == "__main__":
    create_app().run()