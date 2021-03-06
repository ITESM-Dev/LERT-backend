from flask import Blueprint, jsonify
import flask
from flask_cors import cross_origin
import flask_login
import requests
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.expense.models import Expense
from LERT.endpoints.ica.models import ICA
from LERT.endpoints.icaAdmin.models import ICAAdmin
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.opmanager.models import OpManager
from LERT.endpoints.user.models import User
from LERT.endpoints.currentPeriod.models import CurrentPeriod
from LERT.endpoints.bandType.models import BandType
from LERT.endpoints.hourType.models import HourType
from LERT.endpoints.resourceExpense.models import ResourceExpense
from LERT.endpoints.authorization.roles import opManager_permission, manager_or_OpManager_or_icaAdmin, manager_or_OpManager
import datetime

opManager = Blueprint('opManager', __name__)

@opManager.route("/getBandTypes", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_or_OpManager_or_icaAdmin.require(http_exception=403)
def getBandTypes():
    try:
        session = Session(connection.e)

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

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)
    
    session.close()
    return jsonify(bandTypes)
    

@opManager.route("/updateBandType", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def updateBandTypes():
    try:
        session = Session(connection.e)

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

    session.close()
    return "Band Type Updated", 200

@opManager.route("/deleteBandType", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def deleteBandTypes():
    try:
        session = Session(connection.e)

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
 
    session.close()
    return "Band Type Deleted", 200

@opManager.route("/getHourTypes", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_or_OpManager_or_icaAdmin.require(http_exception=403)
def getHourTypes():
    try:
        session = Session(connection.e)

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

    session.close()
    return jsonify(hourTypes)

@opManager.route("/getManagers", methods=['GET'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def getManagers():
    try:
        session = Session(connection.e)

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
                "lastUpdated": str(current.lastUpdated)
            }

            resultManagers.append(currentManager)

    except requests.exceptions.RequestException as e: 
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return jsonify(resultManagers), 200    

@opManager.route("/updateManager", methods=['PATCH'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def updateManager():
    try:
        session = Session(connection.e)

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

    session.close()
    return statusCode  
    
@opManager.route("/updateHourType", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def updateHourType():
    try:
        session = Session(connection.e)

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

    session.close()
    return "Hour Type Updated", 200

@opManager.route("/deleteHourType", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def deleteHourType():
    try:
        session = Session(connection.e)

        hourTypeIdReq = int(flask.request.json['id'])
        hourTypeDB = session.query(HourType).filter_by(idHourType = hourTypeIdReq).first()
        
        session.delete(hourTypeDB)
        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    session.close()
    return "Hour Type Deleted", 200

@opManager.route("/getCurrentPeriods", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_or_OpManager_or_icaAdmin.require(http_exception=403)
def getCurrentPeriods():
    try:
        session = Session(connection.e)

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

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return jsonify(currentPeriods)

@opManager.route("/updateCurrentPeriod", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def updateCurrentPeriod():
    try:
        session = Session(connection.e)

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

    session.close()
    return "Current Period Updated", 200

@opManager.route("/deleteCurrentPeriod", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def deleteCurrentPeriod():
    try:
        session = Session(connection.e)

        currentPeriodIdReq = int(flask.request.json['id'])
        currentPeriodDB = session.query(CurrentPeriod).filter_by(idCurrentPeriod = currentPeriodIdReq).first()
        
        session.delete(currentPeriodDB)
        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    session.close()
    return "Current Period Deleted", 200

@opManager.route("/getIcas", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_or_OpManager_or_icaAdmin.require(http_exception=403)
def getIcas():
    try:
        session = Session(connection.e)
        
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

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return jsonify(icas)

@opManager.route("/updateIca", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def updateIca():
    try:
        session = Session(connection.e)

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

    session.close()
    return "ICA Updated", 200

@opManager.route("/deleteIca", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def deleteIca():
    try:
        session = Session(connection.e)

        icaIdReq = int(flask.request.json['id'])
        icaDB = session.query(ICA).filter_by(idICA = icaIdReq).first()
        
        session.delete(icaDB)
        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    session.close()
    return "ICA Deleted", 200

@opManager.route("/getAvailableManagersICA", methods=['GET'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def getAvailableManagersICA():
    try:
        session = Session(connection.e)

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

    session.close()
    return jsonify(managers), 200

@opManager.route("/getManagersNoOpManager", methods=['GET'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def getManagersNoOpManager():
    try:
        session = Session(connection.e)

        managersDB = session.query(Manager).filter_by(idOPManager = None).all()
        
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

    session.close()
    return jsonify(managers), 200

@opManager.route("/getManagersNoIcaAdmins", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_or_OpManager.require(http_exception=403)
def getManagersNoIcaAdmins():
    try:
        session = Session(connection.e)

        managersDB = session.query(Manager).filter_by(idICA_Admin = None).all()
        
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

    session.close()
    return jsonify(managers), 200

@opManager.route("/getManagerAndIcaAdmins", methods=['GET'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def getManagerAndIcaAdmins():
    try:
        session = Session(connection.e)

        managersDB = session.query(Manager).filter(Manager.idICA_Admin != None).all()
        
        managers = []

        for manager in managersDB:
            
            
            managerQuery = session.query(Manager).filter_by(idManager = manager.idManager).first()
            managerMailQuery = session.query(User).filter_by(idUser = managerQuery.idUser).first()

            icaAdminIDUser = session.query(ICAAdmin).filter_by(idICA_Admin = manager.idICA_Admin).first()
            icaAdminMail = session.query(User).filter_by(idUser = icaAdminIDUser.idUser).first()

            if managerQuery == None or icaAdminIDUser == None:
                continue
                
            currentManager = {
                "managerMail": managerMailQuery.mail,
                "icaAdminMail": icaAdminMail.mail,

            }

            managers.append(currentManager)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return jsonify(managers), 200

@opManager.route("/getICAAdmins", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_or_OpManager.require(http_exception=403)
def geICAAdmins():
    try:
        session = Session(connection.e)

        icaAdminDB = session.query(ICAAdmin).all()
        
        icaAdmins = []

        for icaAdmin in icaAdminDB:

            icaAdminIDUser = session.query(User).filter_by(idUser = icaAdmin.idUser).first()
            
            if icaAdminIDUser == None:
                continue

            currentIcaAdmin = {
                "mail": icaAdminIDUser.mail
            }

            icaAdmins.append(currentIcaAdmin)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return jsonify(icaAdmins), 200

@opManager.route("/OpAssignIcaAdminManager", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def OpAssignIcaAdminManager():
    try:
        session = Session(connection.e)

        icaAdminMailReq = flask.request.json['icaAdminMail']
        managerMailReq = flask.request.json['managerMail']
        
        icaAdminUserQuery = session.query(User).filter_by(mail = icaAdminMailReq).first()
        managerUserQuery = session.query(User).filter_by(mail = managerMailReq).first()
        
        
        if icaAdminUserQuery == None or managerUserQuery == None:
            return "Ica Admin or Manager does not exist"
        
        icaAdminId = session.query(ICAAdmin).filter_by(idUser = icaAdminUserQuery.idUser).first().idICA_Admin
        
        session.query(Manager).\
            filter_by(idUser = managerUserQuery.idUser).\
            update({
                Manager.idICA_Admin: icaAdminId
            })

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    session.close()
    return "ICA Admin assigned to Manager", 200

@opManager.route("/deleteManagerFromOPManager", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def deleteManagerFromOPManager():
    try:
        session = Session(connection.e)
        
        managerMailReq = flask.request.json['managerMail']
        
        managerUserQuery = session.query(User).filter_by(mail = managerMailReq).first()
        
        if managerUserQuery == None:
            return "Manager does not exist"
        
        
        session.query(Manager).\
            filter_by(idUser = managerUserQuery.idUser).\
            update({
                Manager.idOPManager: None
            })

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    session.close()
    return "Manager unassigned", 200
