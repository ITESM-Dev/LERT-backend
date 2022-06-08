from crypt import methods
from flask import Blueprint
import flask_login
from flask_cors import cross_origin
import flask
from sqlalchemy.orm import Session
from LERT.db.database import connection
import requests
from LERT.endpoints.currentPeriod.models import CurrentPeriod
from LERT.endpoints.authorization.roles import opManager_permission

currentPeriod = Blueprint('currentPeriod', __name__)

session = Session(connection.e)

@currentPeriod.route("/createCurrentPeriod", methods = ['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def createCurrentPeriod():

    statusCode = flask.Response(status=201)
    quarterReq = int(flask.request.json['quarter'])
    yearReq = int(flask.request.json['year'])
    keyReq = int(flask.request.json['key'])
    statusReq = flask.request.json['status']

    try:
        
        currentPeriod1 = CurrentPeriod(quarter = quarterReq, year = yearReq, key = keyReq, status = statusReq)
        session.add(currentPeriod1)
        session.commit() 
        
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)


    id = {"id": currentPeriod1.idCurrentPeriod }
    
    return id, 201 

session.close()