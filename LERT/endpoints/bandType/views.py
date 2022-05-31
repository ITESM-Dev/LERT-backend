from crypt import methods
from flask import Blueprint
import flask_login
from flask_cors import cross_origin
import flask
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.bandType.models import BandType
import requests
bandType = Blueprint('bandType', __name__)

session = Session(connection.e)

@bandType.route("/createBandType", methods=['POST'])
@cross_origin()
@flask_login.login_required
def createBandType():

    statusCode = flask.Response(status=201)
    typeReq = flask.request.json['type']
    bandReq = flask.request.json['band'] 
    yearlyRateReq = int(flask.request.json['yearlyRate'])
    countryReq = flask.request.json['country']
    dateToStartReq = flask.request.json['dateToStart']

    try:
        session = Session(connection.e)

        bandType1 = BandType(type = typeReq, band = bandReq, yearlyRate = yearlyRateReq, country = countryReq, dateToStart = dateToStartReq)
        session.add(bandType1)
        session.commit() 
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)    
    except Exception as e:
        print(e)

    return statusCode

session.close()

