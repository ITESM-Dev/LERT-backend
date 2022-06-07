from sys import stderr
from turtle import TPen
from flask import Blueprint, jsonify
import flask
from flask_cors import cross_origin
import flask_login
import requests
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.expense.models import Expense
from LERT.endpoints.ica.models import ICA
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.opmanager.models import OpManager
from LERT.endpoints.user.models import User
from LERT.endpoints.currentPeriod.models import CurrentPeriod
from LERT.endpoints.bandType.models import BandType
from LERT.endpoints.hourType.models import HourType
from LERT.endpoints.resourceExpense.models import ResourceExpense
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

        bandTypeIDReq = int(flask.request.json['id'])
        bandTypeDB = session.query(BandType).filter_by(idBandType = bandTypeIDReq).first()
        hourType = session.query(HourType).filter_by(idBandType = bandTypeDB.idBandType).first()        
        resourceExpense = session.query(ResourceExpense).filter_by(idHourType = hourType.idHourType)

        resourceExpense.update({ResourceExpense.idHourType:None})
        hourType.idBandType = None

        session.commit()
        session.delete(bandTypeDB)
        session.delete(hourType)
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
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return jsonify(hourTypes)

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

@opManager.route("/getCurrentPeriods", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getCurrentPeriods():
    try:
        currentPeriodsDB = session.query(CurrentPeriod).all()
        currentPeriods = []
        for currentPeriodDB in currentPeriodsDB:
            currentPeriod = {
                "id" : currentPeriodDB.idCurrentPeriod,
                "quarter": currentPeriodDB.quarter,
                "year": currentPeriodDB.year,
                "key": currentPeriodDB.key,
                "status": currentPeriodDB.status
            }
            currentPeriods.append(currentPeriod)

        return jsonify(currentPeriods)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

@opManager.route("/updateCurrentPeriod", methods=['POST'])
@cross_origin()
@flask_login.login_required
def updateCurrentPeriod():
    try:
        currentPeriodIdReq = int(flask.request.json['id'])
        quarterReq = int(flask.request.json['quarter'])
        yearReq = int(flask.request.json['year'])
        keyReq = int(flask.request.json['key'])
        statusReq = flask.request.json['status']

        session.query(CurrentPeriod).\
            filter_by(idCurrentPeriod = currentPeriodIdReq).\
            update({CurrentPeriod.quarter: quarterReq, CurrentPeriod.year: yearReq,
            CurrentPeriod.key:keyReq, CurrentPeriod.status: statusReq})

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    return "Current Period Updated", 200

@opManager.route("/deleteCurrentPeriod", methods=['POST'])
@cross_origin()
@flask_login.login_required
def deleteCurrentPeriod():
    try:
        currentPeriodIdReq = int(flask.request.json['id'])
        currentPeriodDB = session.query(CurrentPeriod).filter_by(idCurrentPeriod = currentPeriodIdReq).first()
        session.delete(currentPeriodDB)
        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    return "Current Period Deleted", 200

@opManager.route("/getIcas", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getIcas():
    try:
        
        icasDB = session.query(ICA).all()
        icas = []
        for ica in icasDB:

            currentIca = {
                "id": ica.idICA,
                "icaCode": ica.icaCode,
                "icaCore": ica.icaCore,
                "year": ica.year,
                "totalBilling": 0,
                "rCtyPerf": ica.rCtyPerf,
                "ctyNamePerf": ica.ctyNamePerf,
                "endDate": str(ica.endDate),
                "startDate": str(ica.startDate),
                "totalPlusTaxes": 0,
                "nec": ica.nec,
                "type": ica.type,
                "description": ica.description,
                "leru": ica.leru,
                "minor": ica.minor,
                "major": ica.major,
                "division":  ica.division,
                "rCtyReq": ica.rCtyReq,
                "ctyNameReq": ica.ctyNameReq,
                "cc": ica.cc,
                "frequencyBill": ica.frequencyBill,
                "depto": ica.depto,
                "status": ica.status,
                "country": ica.country,
                "budget": ica.budget,
                "icaOwner": ica.icaOwner,
                "idPlanning": ica.idPlanning
            }


            totalBilling = 0

            managers = session.query(Manager).filter_by(idICA = ica.idICA).all()

            if managers != None:
                for manager in managers:
                    expenses = session.query(Expense).filter_by(idManager = manager.idManager).all()
                    if expenses != None:
                        for expense in expenses:
                            totalBilling += expense.cost
                ica.totalBilling = totalBilling
                ica.totalPlusTaxes = totalBilling * 1.16
                session.commit()

                currentIca['totalBilling'] = totalBilling
                currentIca['totalPlusTaxes'] = totalBilling * 1.16

            icas.append(currentIca)

        return jsonify(icas)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

@opManager.route("/updateIca", methods=['POST'])
@cross_origin()
@flask_login.login_required
def updateIca():
    try:
        idIcaReq = flask.request.json['id']
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

        y, m, d = startDateReq.split('-')
        startDate = datetime.datetime(int(y), int(m), int(d))

        y, m, d = endDateReq.split('-')
        endDate = datetime.datetime(int(y), int(m), int(d))

        previousOwner = session.query(ICA).filter_by(idICA = idIcaReq).first().icaOwner

        session.query(ICA).\
            filter_by(idICA = idIcaReq).\
            update({ICA.icaCode: icaCodeReq, ICA.icaCore: icaCoreReq, ICA.year: yearReq, ICA.idPlanning: idPlanningReq,
            ICA.icaOwner: icaOwnerReq, ICA.budget: budgetReq, ICA.country: countryReq, ICA.status:statusReq,
            ICA.depto: deptoReq, ICA.frequencyBill: frequencyBillReq, ICA.cc: ccReq, ICA.ctyNameReq: ctyNameReq1,
            ICA.rCtyReq: rCtyReq1, ICA.division: divisionReq, ICA.major: majorReq, ICA.minor: minorReq, 
            ICA.leru: leruReq, ICA.description: descriptionReq, ICA.type: typeReq, ICA.nec: necReq, 
            ICA.totalPlusTaxes: totalPlusTaxesReq, ICA.startDate: startDate, ICA.endDate: endDate, ICA.ctyNamePerf: ctyNamePerfReq,
            ICA.rCtyPerf: rCtyPerfReq, ICA.totalBilling: totalBillingReq})

        
        managerID = session.query(User).filter_by(mail = icaOwnerReq).first().idUser
        previousManagerID = session.query(User).filter_by(mail = previousOwner).first().idUser
        
        session.query(Manager).\
            filter_by(idUser = managerID).\
            update({Manager.idICA: idIcaReq})

        session.query(Manager).\
            filter_by(idUser = previousManagerID).\
            update({Manager.idICA: None})

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    return "ICA Updated", 200

@opManager.route("/deleteIca", methods=['POST'])
@cross_origin()
@flask_login.login_required
def deleteIca():
    try:
        icaIdReq = int(flask.request.json['id'])
        icaDB = session.query(ICA).filter_by(idICA = icaIdReq).first()
        session.delete(icaDB)
        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    return "ICA Deleted", 200

@opManager.route("/getAvailableManagersICA", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getAvailableManagersICA():
    try:
        managersDB = session.query(Manager).filter_by(idICA = None).all()
        
        managers = []

        for manager in managersDB:

            managerIDUser = session.query(Manager).filter_by(idManager = manager.idManager).first().idUser
            managerMail = session.query(User).filter_by(idUser = managerIDUser).first().mail
            
            currentManager = {
                "mail": managerMail
            }

            managers.append(currentManager)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return jsonify(managers), 200

session.close()
