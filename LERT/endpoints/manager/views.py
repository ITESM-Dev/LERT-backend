from crypt import methods
from sys import stderr
from flask import Blueprint
import flask
import flask_login
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.opmanager.models import OpManager
from LERT.endpoints.icaAdmin.models import ICAAdmin
from LERT.endpoints.user.models import User
from LERT.endpoints.authorization.roles import opManager_permission, icaAdmin_permission
from flask_cors import cross_origin

manager = Blueprint('manager', __name__)

session = Session(connection.e)

@manager.route("/setOpManager", methods=['POST'])
@cross_origin()
@flask_login.login_required
def setOpManager():
    managerMail = flask.request.json['managerMail']
    opManagerMail = flask_login.current_user.id

    managerQuery = session.query(User).filter_by(mail = managerMail)
    opManagerUserQuery = session.query(User).filter_by(mail = opManagerMail)
    opManagerUserID = opManagerUserQuery.first().idUser
    opManagerQuery = session.query(OpManager).filter_by(idUser = opManagerUserID)
    opManagerID = opManagerQuery.first().idOPManager
    managerID = managerQuery.first().idUser
    
    session.query(Manager).\
        filter_by(idManager = managerID).\
        update({Manager.idOPManager: opManagerID})
    session.commit()

    return "Manager assigned to OpManager", 200

@manager.route("/setIcaAdmin", methods=['POST'])
@cross_origin()
@flask_login.login_required
def setIcaAdmin():
    managerMail = flask.request.json['managerMail']
    icaAdminMail = flask_login.current_user.id

    managerQuery = session.query(User).filter_by(mail = managerMail)
    icaAdminUserQuery = session.query(User).filter_by(mail = icaAdminMail)
    icaAdminUserID = icaAdminUserQuery.first().idUser
    icaAdminQuery = session.query(ICAAdmin).filter_by(idUser = icaAdminUserID)
    icaAdminID = icaAdminQuery.first().idICA_Admin
    managerID = managerQuery.first().idUser
    
    session.query(Manager).\
        filter_by(idManager = managerID).\
        update({Manager.idICA_Admin: icaAdminID})
    session.commit()

    return "Manager assigned to IcaAdmin", 200

    
session.close()