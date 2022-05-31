from flask import Blueprint
from crypt import methods
import flask_login
from flask_cors import cross_origin
import flask
from sqlalchemy.orm import Session
from LERT.db.database import connection
import requests
from LERT.endpoints.ica.models import ICA
import datetime

ica = Blueprint('ica', __name__)

session = Session(connection.e)

@ica.route("/createIca", methods = ['POST'])
@cross_origin()
@flask_login.login_required
def createCurrentPeriod():
    
    statusCode = flask.Response(status=201)
    icaCodeReq = flask.request.json['icaCode']
    icaCoreReq = flask.request.json['icaCore']
    yearReq = flask.request.json['year']
    idPlanningReq = flask.request.json['idPlanning']
    icaOwnerReq = flask.request.json['icaOwner']
    budgetReq = int(flask.request.json['budget'])
    countryReq = flask.request.json['country']
    statusReq = flask.request.json['status']
    deptoReq = flask.request.json['depto']
    frequencyBillReq = flask.request.json['frequencyBill']
    ccReq = flask.request.json['cc']
    ctyNameReq1 = flask.request.json['ctyNameReq']
    rCtyReq1 = flask.request.json['rCtyReq']
    divisionReq = flask.request.json['division']
    majorReq = flask.request.json['major']
    minorReq = flask.request.json['minor']
    leruReq = flask.request.json['leru']
    descriptionReq = flask.request.json['description']
    typeReq  = flask.request.json['type']
    necReq = int(flask.request.json['nec'])
    totalPlusTaxesReq  = int(flask.request.json['totalPlusTaxes'])
    startDateReq = flask.request.json['startDate']
    endDateReq = flask.request.json['endDate']
    ctyNamePerfReq = flask.request.json['ctyNamePerf']
    rCtyPerfReq = flask.request.json['rCtyPerf']
    totalBillingReq = int(flask.request.json['totalBilling'])
    
    try:
        y, m, d = startDateReq.split('-')
        startDateReq = datetime.datetime(int(y), int(m), int(d))

        y, m, d = endDateReq.split('-')
        endDateReq = datetime.datetime(int(y), int(m), int(d))
        
        ica1 = ICA(
            icaCode = icaCodeReq,
            icaCore = icaCoreReq,
            year = yearReq,
            idPlanning = idPlanningReq,
            icaOwner = icaOwnerReq,
            budget = budgetReq,
            country = countryReq,
            status = statusReq,
            depto = deptoReq,
            frequencyBill = frequencyBillReq,
            cc = ccReq,
            ctyNameReq = ctyNameReq1,
            rCtyReq = rCtyReq1,
            division = divisionReq,
            major = majorReq,
            minor = minorReq,
            leru = leruReq,
            description = descriptionReq,
            type = typeReq,
            nec = necReq,
            totalPlusTaxes = totalPlusTaxesReq,
            startDate = startDateReq,
            endDate = endDateReq,
            ctyNamePerf = ctyNamePerfReq,
            rCtyPerf = rCtyPerfReq,
            totalBilling = totalBillingReq
        )

        session.add(ica1)
        session.commit() 
        
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)


    return statusCode

session.close()