from crypt import methods
from sys import stderr
from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.opmanager.models import OpManager
from flask_cors import cross_origin
import requests
import flask_login
from LERT.endpoints.bandType.models import BandType

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

session.close()