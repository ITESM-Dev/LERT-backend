from crypt import methods
from sys import stderr
from flask import Blueprint, jsonify
import flask
import flask_login
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.ica.models import ICA
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.opmanager.models import OpManager
from LERT.endpoints.icaAdmin.models import ICAAdmin
from LERT.endpoints.user.models import User
from LERT.endpoints.resource.models import Resource
from LERT.endpoints.manager.models import association_table_Manager_Resource
from LERT.endpoints.authorization.roles import opManager_permission, icaAdmin_permission
from flask_cors import cross_origin
import requests

manager = Blueprint('manager', __name__)

session = Session(connection.e)

@manager.route("/setOpManager", methods=['POST'])
@cross_origin()
@flask_login.login_required
def setOpManager():
    try:
        managerMail = flask.request.json['managerMail']
        opManagerMail = flask_login.current_user.id

        managerQuery = session.query(User).filter_by(mail = managerMail)
        opManagerUserQuery = session.query(User).filter_by(mail = opManagerMail)
        opManagerUserID = opManagerUserQuery.first().idUser
        opManagerQuery = session.query(OpManager).filter_by(idUser = opManagerUserID)
        opManagerID = opManagerQuery.first().idOPManager
        managerID = managerQuery.first().idUser

        
        session.query(Manager).\
            filter_by(idUser = managerID).\
            update({Manager.idOPManager: opManagerID})

        session.commit()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return "Manager assigned to OpManager", 200

@manager.route("/setIcaAdmin", methods=['POST'])
@cross_origin()
@flask_login.login_required
def setIcaAdmin():
    try:
        managerMail = flask.request.json['managerMail']
        icaAdminMail = flask_login.current_user.id

        managerQuery = session.query(User).filter_by(mail = managerMail)
        icaAdminUserQuery = session.query(User).filter_by(mail = icaAdminMail)
        icaAdminUserID = icaAdminUserQuery.first().idUser
        icaAdminQuery = session.query(ICAAdmin).filter_by(idUser = icaAdminUserID)
        icaAdminID = icaAdminQuery.first().idICA_Admin
        managerID = managerQuery.first().idUser
        
        session.query(Manager).\
            filter_by(idUser = managerID).\
            update({Manager.idICA_Admin: icaAdminID})
        session.commit()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return "Manager assigned to IcaAdmin", 200

@manager.route("/assignResourceToManager", methods=['POST'])
@cross_origin()
@flask_login.login_required
def assignResourceToManager():
    try:
        managerMail = flask_login.current_user.id
        resourceMailReq = flask.request.json['resourceMail']

        resourceUserID = session.query(User).filter_by(mail = resourceMailReq).first().idUser
        resourceID = session.query(Resource).filter_by(idUser = resourceUserID).first().idSerial

        print(resourceID, file=stderr)

        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser
        managerID = session.query(Manager).filter_by(idUser = managerUserID).first().idManager
        print(managerID, file=stderr)

        
        association_manager_resource = association_table_Manager_Resource.insert().values(idSerial = resourceID, idManager = managerID)
        session.execute(association_manager_resource) 
        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return "OK", 200

@manager.route("/getManagerICA", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getManagerICA():
    try:
        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser
        managerIDICA = session.query(Manager).filter_by(idUser = managerUserID).first().idICA
        managerICACode = session.query(ICA).filter_by(idICA = managerIDICA).first().icaCode
        
        resultICA = {
            "idICA" : managerIDICA,
            "icaCode": managerICACode
        }
     
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return resultICA, 200

@manager.route("/getAvailableResources", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getAvailableResources():
    try:
        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser
        managerID = session.query(Manager).filter_by(idUser = managerUserID).first().idManager

        resources = session.query(association_table_Manager_Resource).filter(association_table_Manager_Resource.c.idManager != managerID).all()
        
        resultResources = []

        for current in resources:

            currResourceIDUser = session.query(Resource).filter_by(idSerial = current.idSerial).first().idUser
            currResourceMail = session.query(User).filter_by(idUser = currResourceIDUser).first().mail
            
            currentResource = {
                "mail": currResourceMail
            }

            resultResources.append(currentResource)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return jsonify(resultResources), 200
    
session.close()