from sys import stderr
from flask import Blueprint
import flask_login
from flask_cors import cross_origin
import flask
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.hourType.models import HourType
from LERT.endpoints.bandType.models import BandType
import requests
import datetime

hourType = Blueprint('hourType', __name__)

session = Session(connection.e)

@hourType.route("/createHourType", methods=['POST'])
@cross_origin()
@flask_login.login_required
def createHourType():
    statusCode = flask.Response(status=201)
    typeReq = flask.request.json['type']
    bandReqName = flask.request.json['band'] 
    rateReq = int(flask.request.json['rate'])
    countryReq = flask.request.json['country']
    dateToStartReq = flask.request.json['dateToStart']
    dateToFinishReq = flask.request.json['dateToFinish']
    
    try:
        
        bandTypeDB = session.query(BandType).filter_by(band = bandReqName, country = countryReq).first()
        bandTypeIDdb = bandTypeDB.idBandType
        
        session.commit() 
        
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    try:

        y, m, d = dateToStartReq.split('-')
        startDateReq = datetime.datetime(int(y), int(m), int(d))

        y, m, d = dateToFinishReq.split('-')
        endDateReq = datetime.datetime(int(y), int(m), int(d))

        hourType1 = HourType(idBandType = bandTypeIDdb, 
            type = typeReq, band = bandReqName, rate = rateReq, 
            country = countryReq, dateToStart = startDateReq, 
            dateToFinish = endDateReq)
        # TODO calculate hourType rate based on bandType yearly rate, country and # of extra hours worked
        session.add(hourType1)
        session.commit() 
        
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)    
    except Exception as e:
        print(e)

    id = {"id": hourType1.idHourType }
    
    return id, 201 

session.close()
