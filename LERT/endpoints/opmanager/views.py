from flask import Blueprint
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.opmanager.models import OpManager
from LERT.endpoints.manager.models import Manager
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

        return "Manager assigned", 200

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

session.close()
