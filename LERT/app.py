from LERT.db import database, session
from LERT.endpoints.ica.views import ica
from LERT.endpoints.opmanager.views import opManager
from LERT.endpoints.manager.views import manager
from LERT.endpoints.expenseType.views import expenseType
from LERT.endpoints.hourType.views import hourType
from LERT.endpoints.bandType.views import bandType
from LERT.endpoints.user.models import User
from LERT.endpoints.user.views import user
from LERT.endpoints.administrator.views import admin
from LERT.endpoints.icaAdmin.views import icaAdmin
from LERT.endpoints.resource.views import resource
from LERT.endpoints.expense.views import expense
from LERT.endpoints.resourceExpense.views import resourceExpense
from LERT.endpoints.currentPeriod.views import currentPeriod
from LERT.db.database import connection
from crypt import methods
import os
import secrets
import time
from flask import Flask
import flask
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
app.register_blueprint(currentPeriod)

login_manager = LoginManager()
login_manager.init_app(app)

VIDA_TOKEN = 1000 * 60 * 3

session2 = Session(connection.e)

@login_manager.user_loader
def load_user(idUser):  
    user = session2.query(User).get(idUser)

    if user == None:
        return "User not found", 401

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
        userDBQuery = session2.query(User).filter_by(mail = userMail)
        userDB = userDBQuery.first()
        userMail = userDB.mail
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

    userDBQuery.\
        update({User.expiration: currentTimestamp}, synchronize_session='fetch')

    
    result = User()
    result.id = userMail
    result.role = userRole

    identity_changed.send(current_app._get_current_object(), identity=Identity(userDB.idUser))

    return result

principals = Principal(app)
principals._init_app(app)
admin_permission = Permission(RoleNeed('Admin'))
opManager_permission = Permission(RoleNeed('OpManager'))
manager_permission = Permission(RoleNeed('Manager'))
icaAdmin_permission = Permission(RoleNeed('IcaAdmin'))
manager_or_IcaAdmin = Permission(RoleNeed('Manager'), RoleNeed('IcaAdmin'))

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):

    try:
        userDBQuery = session2.query(User).filter_by(idUser = identity.id).first()

        # Add the UserNeed to the identity
        if hasattr(identity, 'id'):
            identity.provides.add(UserNeed(userDBQuery.idUser))

        # Assuming the User model has a list of roles, update the
        # identity with the roles that the user provides
        
        identity.provides.add(RoleNeed(userDBQuery.role))
    except Exception as e:
        return e

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    
    try:
        userMail = flask.request.json['mail']
        userDBQuery = session2.query(User).filter_by(mail = userMail)
        userDB = userDBQuery.first()
        userMail = userDB.mail
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

    userDBQuery.\
        update({User.token: ph.hash(token)}, synchronize_session='fetch')
    
    userDBQuery.\
        update({User.expiration: expiration}, synchronize_session='fetch')

    session2.commit()  

    print(userDB.mail, file=sys.stderr)

    result = {
        "id": userDB.idUser,
        "name": userDB.name,
        "mail": userDB.mail,
        "role": userDB.role,
        "country": userDB.country,
        "token": token
    }

    return result, 200

@app.route('/protegido')
@cross_origin()
@login_required
@admin_permission.require(http_exception=403)
def protegido():

    return(flask_login.current_user.role)

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
    userDBQuery = session2.query(User).filter_by(mail = flask_login.current_user.id)
    userDBQuery.\
        update({User.expiration: 0}, synchronize_session='fetch')
    return "Logged Out", 200

session2.close()

if __name__ == "__main__":
    create_app().run()