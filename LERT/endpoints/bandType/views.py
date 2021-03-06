from crypt import methods
from sys import stderr
from flask import Blueprint
import flask_login
from flask_cors import cross_origin
import flask
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.bandType.models import BandType
import requests
import datetime
from LERT.endpoints.authorization.roles import opManager_permission

bandType = Blueprint('bandType', __name__)

@bandType.route("/createBandType", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def createBandType():

    typeReq = flask.request.json['type']
    bandReq = flask.request.json['band'] 
    yearlyRateReq = int(flask.request.json['yearlyRate'])
    countryReq = flask.request.json['country']
    dateToStartReq = flask.request.json['dateToStart']
    dateToFinishReq = flask.request.json['dateToFinish']

    try:
        session = Session(connection.e)

        y, m, d = dateToStartReq.split('-')
        startDateReq = datetime.datetime(int(y), int(m), int(d))

        y, m, d = dateToFinishReq.split('-')
        endDateReq = datetime.datetime(int(y), int(m), int(d))

        bandType1 = BandType(type = typeReq, band = bandReq, yearlyRate = yearlyRateReq, country = countryReq, dateToStart = startDateReq, dateToFinish = endDateReq)
        session.add(bandType1)
        session.commit() 
        
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)    
    except Exception as e:
        print(e)

    id = {"id": bandType1.idBandType }

    session.close()    
    return id, 201

