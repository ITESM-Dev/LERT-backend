from sys import stderr
from flask import Blueprint, jsonify
import flask
from flask_cors import cross_origin
import flask_login
import requests
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.opmanager.models import OpManager
from flask_cors import cross_origin
from LERT.endpoints.ica.models import ICA
from LERT.endpoints.user.models import User
import requests
import flask_login
import flask

opManager = Blueprint('opManager', __name__)

session = Session(connection.e)

@opManager.route("/assignIcaToManager", methods=['POST'])
@cross_origin()
@flask_login.login_required
def assignIcaToManager():
    try:
        icaCodeReq = flask.request.json['icaCode']
        managerMailReq = flask.request.json['managerMail']
        idIcaDB = session.query(ICA).filter_by(icaCode = icaCodeReq).first().idICA

        idManagerUser = session.query(User).filter_by(mail = managerMailReq).first().idUser
        idManager = session.query(Manager).filter_by(idUser = idManagerUser).first().idManager

        session.query(Manager).\
            filter_by(idManager = idManager).\
            update({Manager.idICA: idIcaDB})
        
        session.commit()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)
        return "Manager assigned", 200

@opManager.route("/getManagers", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getManagers():
    try:
        opManagerMail = flask_login.current_user.id
        opManagerUserID =  session.query(User).filter_by(mail = opManagerMail).first().idUser
        opManagerID = session.query(OpManager).filter_by(idUser = opManagerUserID).first().idOPManager
        managers = session.query(Manager).filter_by(idOPManager = opManagerID).all()

        resultManagers = []

        for current in managers:

            currentMail =  session.query(User).get(current.idUser).mail
            
            currentManager = {
                "id": current.idManager,
                "mail": currentMail,
                "status": current.status,
                "recoveryStatus": current.recoveryStatus,
                "lastUpdated": current.lastUpdated
            }

            resultManagers.append(currentManager)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)
    return jsonify(resultManagers), 200    

@opManager.route("/updateManager", methods=['PATCH'])
@cross_origin()
@flask_login.login_required
def updateManager():
    try:
        statusCode = flask.Response(status=201)
        managerMailReq = flask.request.json['mail']
        managerStatusReq = flask.request.json['status']
        opManagerMail = flask_login.current_user.id

        managerUserID = session.query(User).filter_by(mail = managerMailReq).first().idUser
        managerOpManID = session.query(Manager).filter_by(idUser = managerUserID).first().idOPManager
        opManagerUserID = session.query(User).filter_by(mail = opManagerMail).first().idUser
        opManagerID = session.query(OpManager).filter_by(idUser = opManagerUserID).first().idOPManager

        if managerOpManID == opManagerID:
            managerDBQuery =  session.query(Manager).filter_by(idUser = managerUserID)

            managerDBQuery.\
                update({Manager.status: managerStatusReq}, synchronize_session='fetch')

            session.commit()  

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return statusCode  
    
session.close()
