from crypt import methods
from sys import stderr
from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.opmanager.models import OpManager
from LERT.endpoints.bandType.models import BandType
from LERT.endpoints.hourType.models import HourType
from flask_cors import cross_origin
import requests
import flask_login
import flask
import datetime

opManager = Blueprint('opManager', __name__)

session = Session(connection.e)

@opManager.route("/getBandTypes", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getBandTypes():
    try:
        bandTypesDB = session.query(BandType).all()
        bandTypes = []
        for band in bandTypesDB:
            currentBand = {
                "id" : band.idBandType,
                "type": band.type,
                "country": band.country,
                "band": band.band,
                "yearlyRate": band.yearlyRate,
                "dateToStart": str(band.dateToStart),
                "dateToFinish": str(band.dateToFinish)
            }
            bandTypes.append(currentBand)

        return jsonify(bandTypes)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

@opManager.route("/updateBandType", methods=['POST'])
@cross_origin()
@flask_login.login_required
def updateBandTypes():
    try:
        bandTypeIdReq = int(flask.request.json['id'])
        typeReq = flask.request.json['type']
        bandReq = flask.request.json['band']
        countryReq = flask.request.json['country']
        yearlyRateReq = int(flask.request.json['yearlyRate'])
        dateToStartReq = flask.request.json['dateToStart']
        dateToFinishReq = flask.request.json['dateToFinish']

        y, m, d = dateToStartReq.split('-')
        startDateReq = datetime.datetime(int(y), int(m), int(d))

        y, m, d = dateToFinishReq.split('-')
        endDateReq = datetime.datetime(int(y), int(m), int(d))

        session.query(BandType).\
            filter_by(idBandType = bandTypeIdReq).\
            update({BandType.type: typeReq, BandType.country:countryReq, BandType.band:bandReq,
            BandType.yearlyRate:yearlyRateReq, BandType.dateToStart: startDateReq, BandType.dateToFinish: endDateReq})

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    return "Band Type Updated", 200

@opManager.route("/deleteBandType", methods=['POST'])
@cross_origin()
@flask_login.login_required
def deleteBandTypes():
    try:
        bandTypeIdReq = int(flask.request.json['id'])
        bandTypeDb = session.query(BandType).filter_by(idBandType = bandTypeIdReq).first()
        session.delete(bandTypeDb)
        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    return "Band Type Deleted", 200

@opManager.route("/getHourTypes", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getHourTypes():
    try:
        hourTypesDB = session.query(HourType).all()
        hourTypes = []
        for hourType in hourTypesDB:
            currentHourType = {
                "id" : hourType.idHourType,
                "type": hourType.type,
                "country": hourType.country,
                "band": hourType.band,
                "rate": hourType.rate,
                "dateToStart": str(hourType.dateToStart),
                "dateToFinish": str(hourType.dateToFinish)
            }
            hourTypes.append(currentHourType)

        return jsonify(hourTypes)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

@opManager.route("/updateHourType", methods=['POST'])
@cross_origin()
@flask_login.login_required
def updateHourType():
    try:
        hourTypeIdReq = int(flask.request.json['id'])
        typeReq = flask.request.json['type']
        bandReq = flask.request.json['band']
        countryReq = flask.request.json['country']
        rateReq = int(flask.request.json['rate'])
        dateToStartReq = flask.request.json['dateToStart']
        dateToFinishReq = flask.request.json['dateToFinish']

        y, m, d = dateToStartReq.split('-')
        startDateReq = datetime.datetime(int(y), int(m), int(d))

        y, m, d = dateToFinishReq.split('-')
        endDateReq = datetime.datetime(int(y), int(m), int(d))

        session.query(HourType).\
            filter_by(idHourType = hourTypeIdReq).\
            update({HourType.type: typeReq, HourType.country:countryReq, HourType.band:bandReq,
            HourType.rate:rateReq, HourType.dateToStart: startDateReq, HourType.dateToFinish: endDateReq})

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    return "Hour Type Updated", 200

@opManager.route("/deleteHourType", methods=['POST'])
@cross_origin()
@flask_login.login_required
def deleteHourType():
    try:
        hourTypeIdReq = int(flask.request.json['id'])
        hourTypeDB = session.query(HourType).filter_by(idHourType = hourTypeIdReq).first()
        session.delete(hourTypeDB)
        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    return "Hour Type Deleted", 200

session.close()