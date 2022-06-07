import secrets
from flask import Blueprint, jsonify
import flask
from flask_cors import cross_origin
import flask_login
import requests
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.icaAdmin.models import ICAAdmin
from sqlalchemy.orm import Session
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.user.models import User

from LERT.endpoints.user.models import User

icaAdmin = Blueprint('icaAdmin', __name__)

session = Session(connection.e)

@icaAdmin.route("/getManagersIcaAdmin", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getManagersIcaAdmin():
    try:
        icaAdminMail = flask_login.current_user.id

        icaAdminUser = session.query(User).filter_by(mail = icaAdminMail).first().idUser
        icaAdminId = session.query(ICAAdmin).filter_by(idUser = icaAdminUser).first().idICA_Admin
        managersIcaAdmin = session.query(Manager).filter_by(idICA_Admin = icaAdminId).all()

        managers = []
        for manager in managersIcaAdmin:
            managerUser = session.query(User).filter_by(idUser = manager.idUser).first()
            currentmanager = {
                "name": managerUser.name,
                "mail": managerUser.mail
            }
            managers.append(currentmanager)

        return jsonify(managers)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    return "ICA Deleted", 200

@icaAdmin.route("/assignTokenAuthenticator", methods=['POST'])
@cross_origin()
@flask_login.login_required
def assignTokenAuthenticator():
    try:
        userMail = flask.request.json['managerMail']
        temporal_token = secrets.token_urlsafe(32)

        managerUserID = session.query(User).filter_by(mail = userMail).first().idUser

        session.query(Manager).filter_by(
            idUser = managerUserID
        ).update(
            {Manager.tokenAuthenticator : temporal_token}
        )
        session.commit()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    return temporal_token, 200
    
session.close()