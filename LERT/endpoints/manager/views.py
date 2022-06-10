import datetime
from sys import stderr
from flask import Blueprint, jsonify, send_file
import flask
import flask_login
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.currentPeriod.models import CurrentPeriod
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.opmanager.models import OpManager
from LERT.endpoints.icaAdmin.models import ICAAdmin
from LERT.endpoints.expenseType.models import ExpenseType
from LERT.endpoints.resourceExpense.models import ResourceExpense
from LERT.endpoints.ica.models import ICA
from LERT.endpoints.icaAdmin.models import ICAAdmin
from LERT.endpoints.expense.models import Expense
from LERT.endpoints.user.models import User
from LERT.endpoints.resource.models import Resource
from LERT.endpoints.expense.models import association_table_Expense_Resource
from LERT.endpoints.manager.models import association_table_Manager_Resource
from LERT.endpoints.authorization.roles import opManager_permission, manager_or_IcaAdmin, manager_permission, manager_or_OpManager
from flask_cors import cross_origin
import requests

manager = Blueprint('manager', __name__)

@manager.route("/setOpManager", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def setOpManager():
    try:
        session = Session(connection.e)

        managerMail = flask.request.json['managerMail']
        opManagerMail = flask_login.current_user.id

        managerQuery = session.query(User).filter_by(mail = managerMail)
        opManagerUserQuery = session.query(User).filter_by(mail = opManagerMail)
        opManagerUserID = opManagerUserQuery.first().idUser
        opManagerQuery = session.query(OpManager).filter_by(idUser = opManagerUserID)
        opManagerID = opManagerQuery.first().idOPManager
        managerID = managerQuery.first().idUser

        
        session.query(Manager).\
            filter_by(idUser = managerID).\
            update({Manager.idOPManager: opManagerID})

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return "Manager assigned to OpManager", 200

@manager.route("/setIcaAdmin", methods=['POST'])
@cross_origin()
@flask_login.login_required
@manager_or_OpManager.require(http_exception=403)
def setIcaAdmin():
    try:
        session = Session(connection.e)

        icaAdminMail = flask.request.json['icaAdminMail']
        managerMail = flask_login.current_user.id

        managerId = session.query(User).filter_by(mail = managerMail).first().idUser
        icaAdminUser = session.query(User).filter_by(mail = icaAdminMail).first().idUser
        icaAdminId = session.query(ICAAdmin).filter_by(idUser = icaAdminUser).first().idICA_Admin
        
        session.query(Manager).\
            filter_by(idUser = managerId).\
            update({Manager.idICA_Admin: icaAdminId})
        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return "IcaAdmin assigned to Manager", 200

@manager.route("/assignResourceToManager", methods=['POST'])
@cross_origin()
@flask_login.login_required
@manager_permission.require(http_exception=403)
def assignResourceToManager():
    try:
        session = Session(connection.e)

        managerMailReq = flask.request.json['managerMail']
        resourceMailReq = flask.request.json['resourceMail']
        bandReq = int(flask.request.json['band'])

        resourceUserID = session.query(User).filter_by(mail = resourceMailReq).first().idUser
        resourceID = session.query(Resource).filter_by(idUser = resourceUserID).first().idSerial

        managerUserID = session.query(User).filter_by(mail = managerMailReq).first().idUser
        managerID = session.query(Manager).filter_by(idUser = managerUserID).first().idManager
        print(managerID, file=stderr)

        
        association_manager_resource = association_table_Manager_Resource.insert().values(idSerial = resourceID, idManager = managerID)
        session.execute(association_manager_resource) 

        session.query(User).\
            filter_by(mail = resourceMailReq).\
            update({User.band: bandReq})

        session.commit()
        session.close()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return "Resource Assigned to Manager", 200

@manager.route("/getManagerICA", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_permission.require(http_exception=403)
def getManagerICA():
    try:
        session = Session(connection.e)

        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser
        managerIDICA = session.query(Manager).filter_by(idUser = managerUserID).first().idICA
        managerICACode = session.query(ICA).filter_by(idICA = managerIDICA).first().icaCode
        
        resultICA = {
            "idICA" : managerIDICA,
            "icaCode": managerICACode
        }
     
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return resultICA, 200

@manager.route("/getAvailableResources", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_permission.require(http_exception=403)
def getAvailableResources():
    try:
        session = Session(connection.e)

        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser
        managerID = session.query(Manager).filter_by(idUser = managerUserID).first().idManager

    
        resources = session.query(Resource).all()

        resultResources = []

        for current in resources:

            resourcesManager = session.query(association_table_Manager_Resource).filter(association_table_Manager_Resource.c.idSerial == current.idSerial).first()

            if resourcesManager != None and resourcesManager.idManager == managerID:
                continue

            currResourceIDUser = session.query(Resource).filter_by(idSerial = current.idSerial).first().idUser
            currResourceMail = session.query(User).filter_by(idUser = currResourceIDUser).first().mail
            
            currentResource = {
                "mail": currResourceMail
            }

            resultResources.append(currentResource)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return jsonify(resultResources), 200
    
@manager.route("/getResources", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_permission.require(http_exception=403)
def getResources():
    try:
        session = Session(connection.e)

        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser
        managerID = session.query(Manager).filter_by(idUser = managerUserID).first().idManager

        print(managerID, file=stderr)

        resources = session.query(association_table_Manager_Resource).filter(association_table_Manager_Resource.c.idManager == managerID).all()
        
        resultResources = []

        for current in resources:

            currResource = session.query(Resource).filter_by(idSerial = current.idSerial).first()
            currResourceUserInfo = session.query(User).filter_by(idUser = currResource.idUser).first()

            currManager = session.query(Manager).filter_by(idManager = current.idManager).first()
            currManagerUserInfo = session.query(User).filter_by(idUser = currManager.idUser).first()

            currManagerICA = session.query(Manager).filter_by(idManager = current.idManager).first().idICA
            ICACode = session.query(ICA).filter_by(idICA = currManagerICA).first().icaCode

            currentResource = {
                "idSerial": currResource.idSerial,
                "mail": currResourceUserInfo.mail,
                "band": currResourceUserInfo.band,
                "managerMail": currManagerUserInfo.mail,
                "icaCode": ICACode
            }

            resultResources.append(currentResource)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return jsonify(resultResources), 200

@manager.route("/getExpenses", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_or_IcaAdmin.require(http_exception=403)
def getExpenses():

    try:
        session = Session(connection.e)

        result_expenses = []
        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser

        queryManager = session.query(Manager).filter_by(idUser = managerUserID).first()
        managerId = queryManager.idManager
        managerIdICA = queryManager.idICA
        managerIdICAAdmin = queryManager.idICA_Admin
        managerIdOPManager = queryManager.idOPManager
        
        expenses = session.query(Expense).filter_by(idManager = managerId).all()


        for expense in expenses:

            expenseType = session.query(ExpenseType).filter_by(idExpenseType = expense.idExpenseType).first().type
            
            if expenseType == "Double" or expenseType == "Triple" or expenseType == "Salary":
                idSerial_ = session.query(association_table_Expense_Resource).filter(association_table_Expense_Resource.c.idExpense == expense.idExpense).first().idResource
                idUser_ = session.query(Resource).filter_by(idSerial = idSerial_).first().idSerial
                user_table = session.query(User).filter_by(idUser = idUser_).first()
                user_id = user_table.idUser
                user_mail = user_table.mail
            else:
                user_id = ""
                user_mail = ""
            idUserICAAdmin = session.query(ICAAdmin).filter_by(idICA_Admin = managerIdICAAdmin).first()
            if(idUserICAAdmin == None):
                mailICAAdmin = None
            else:
                mailICAAdmin = session.query(User).filter_by(idUser = idUserICAAdmin.idUser).first().mail
            idUserOpManager = session.query(OpManager).filter_by(idOPManager = managerIdOPManager).first().idUser
            mailOPManager = session.query(User).filter_by(idUser = idUserOpManager).first().mail
            
            
            current = {
                'id_expense': expense.idExpense,
                "type": expenseType,
                "cost": expense.cost,
                "date": str(expense.date),
                "comment": expense.comment,
                "idICA": managerIdICA,
                "idEmployee": user_id,
                "employeeMail": user_mail,
                "idICAManager": managerIdICAAdmin,
                "ICAManager": mailICAAdmin,
                "idAdministrator": managerIdOPManager,
                "administrator": mailOPManager
            }
            result_expenses.append(current)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()     
    return jsonify(result_expenses), 200

@manager.route("/updateExpense", methods=['POST'])
@cross_origin()
@flask_login.login_required
@manager_or_IcaAdmin.require(http_exception=403)
def updateExpenses():
    try:
        session = Session(connection.e)

        expenseIDReq = int(flask.request.json['id'])
        expenseCostReq = int(flask.request.json['cost'])
        expenseDateReq_unparsed = flask.request.json['date']
        expenseCommentReq = flask.request.json['comment']

        y, m, d = expenseDateReq_unparsed.split('-')
        expenseDateReq = datetime.datetime(int(y), int(m), int(d)).date()

        session.query(Expense).\
                filter_by(idExpense = expenseIDReq).\
                update({Expense.cost: expenseCostReq, Expense.date: expenseDateReq, Expense.comment:expenseCommentReq})

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    except Exception as e:
        print(e) 

    session.close()
    return "Expense updated" ,200

@manager.route("/deleteExpense", methods=['POST'])
@cross_origin()
@flask_login.login_required
@manager_or_IcaAdmin.require(http_exception=403)
def deleteExpenses():
    try:
        session = Session(connection.e)

        expenseIDReq = int(flask.request.json['id'])
        expenseDB = session.query(Expense).filter_by(idExpense = expenseIDReq).first()
        expenseType = session.query(ExpenseType).filter_by(idExpenseType = expenseDB.idExpenseType).first()
        resourceExpense = session.query(ResourceExpense).filter_by(idExpense = expenseDB.idExpense)

        if expenseType == "Salary" or expenseType == "Double" or expenseType == "Triple" : 
            session.delete(resourceExpense.first())
        
        session.delete(expenseDB)
        session.commit() 

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    except Exception as e:
        print(e) 

    session.close()
    return "Expense Deleted", 200

@manager.route("/expensesForQuarter", methods=['POST'])
@cross_origin()
@flask_login.login_required
@manager_or_IcaAdmin.require(http_exception=403)
def expensesForQuarter():
    
    try: 
        session = Session(connection.e)

        expenseYearReq = int(flask.request.json['year'])
        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser

        queryManager = session.query(Manager).filter_by(idUser = managerUserID).first()
        managerId = queryManager.idManager
        expenses = session.query(Expense).filter_by(idManager = managerId).all()
        
        first_quarter = 0
        second_quarter = 0
        third_quarter = 0
        fourth_quarter = 0

        valid_expenses = []
        for expense in expenses:

            expenseCurrentYear = session.query(CurrentPeriod).filter_by(idCurrentPeriod = expense.idCurrentPeriod).first().year
            
            if expenseCurrentYear == expenseYearReq:
                valid_expenses.append(expense)
            
        for valid_expense in valid_expenses:
            expenseCurrentQuarter = session.query(CurrentPeriod).filter_by(idCurrentPeriod = valid_expense.idCurrentPeriod).first().quarter
            
            if int(expenseCurrentQuarter) == 1:
                first_quarter += valid_expense.cost
            elif int(expenseCurrentQuarter) == 2:
                second_quarter += valid_expense.cost
            elif int(expenseCurrentQuarter) == 3:
                third_quarter += valid_expense.cost
            elif int(expenseCurrentQuarter) == 4:
                fourth_quarter += valid_expense.cost
    
        quarters = {
            '1': first_quarter,
            "2": second_quarter,
            "3": third_quarter,
            "4": fourth_quarter,
        }

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    except Exception as e:
        print(e) 

    session.close()
    return quarters, 200
    
@manager.route("/reportExpense", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_or_IcaAdmin.require(http_exception=403)
def reportExpense():
    try: 
        session = Session(connection.e)

        report = []
        startDate = flask.request.json['startDate']
        endDate = flask.request.json['endDate']

        y, m, d = startDate.split('-')
        startDateReq = datetime.datetime(int(y), int(m), int(d))

        y, m, d = endDate.split('-')
        endDateReq = datetime.datetime(int(y), int(m), int(d))

        result_expenses = []
        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser

        queryManager = session.query(Manager).filter_by(idUser = managerUserID).first()
        managerId = queryManager.idManager
        managerIdICA = queryManager.idICA
        managerIdICAAdmin = queryManager.idICA_Admin
        managerIdOPManager = queryManager.idOPManager
        
        expenses = session.query(Expense).filter_by(idManager = managerId).all()


        for expense in expenses:

            expenseType = session.query(ExpenseType).filter_by(idExpenseType = expense.idExpenseType).first().type
            
            if expenseType == "Double" or expenseType == "Triple" or expenseType == "Salary":
                idSerial_ = session.query(association_table_Expense_Resource).filter(association_table_Expense_Resource.c.idExpense == expense.idExpense).first().idResource
                idUser_ = session.query(Resource).filter_by(idSerial = idSerial_).first().idSerial
                user_table = session.query(User).filter_by(idUser = idUser_).first()
                user_id = user_table.idUser
                user_mail = user_table.mail
            else:
                user_id = ""
                user_mail = ""
            

            idUserICAAdmin = session.query(ICAAdmin).filter_by(idICA_Admin = managerIdICAAdmin).first().idUser
            mailICAAdmin = session.query(User).filter_by(idUser = idUserICAAdmin).first().mail
            idUserOpManager = session.query(OpManager).filter_by(idOPManager = managerIdOPManager).first().idUser
            mailOPManager = session.query(User).filter_by(idUser = idUserOpManager).first().mail
            
            current = {
                'id_expense': expense.idExpense,
                "type": expenseType,
                "cost": expense.cost,
                "date": str(expense.date),
                "comment": expense.comment,
                "idICA": managerIdICA,
                "idEmployee": user_id,
                "employeeMail": user_mail,
                "idICAManager": managerIdICAAdmin,
                "ICAManager": mailICAAdmin,
                "idAdministrator": managerIdOPManager,
                "administrator": mailOPManager
            }
            result_expenses.append(current)
        
        for item in result_expenses:
            if item["date"] >= str(startDateReq) and item["date"] <= str(endDateReq):
                report.append(item)

    except requests.exceptions.RequestException as e:  
        raise SystemExit(e)
    except Exception as e:
        print(e) 
    
    session.close()
    return jsonify(report), 200

@manager.route("/getAvailableDelegates", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_or_OpManager.require(http_exception=403)
def getAvailableDelegates():
    
    try:
        session = Session(connection.e)

        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser
        managerQuery = session.query(Manager).filter_by(idUser = managerUserID).first()

        delegates = session.query(User).filter(User.role == "IcaAdmin").all()

        availableDelegates = []

        for currentDelegate in delegates:
            icaAdminID = session.query(ICAAdmin).filter_by(idUser = currentDelegate.idUser).first().idICA_Admin
            
            if managerQuery.idICA_Admin == icaAdminID:
                continue

            delegate = {
                "mail": currentDelegate.mail,
            }

            availableDelegates.append(delegate)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    except Exception as e:
        print(e)
    
    session.close()
    return jsonify(availableDelegates), 200

@manager.route("/getICAAdminManager", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_permission.require(http_exception=403)
def getICAAdminManager():
    try:
        session = Session(connection.e)

        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser
        
        managerIDICA_Admin = session.query(Manager).filter_by(idUser = managerUserID).first()

        resultICA = {
            "idICA_Admin" : None,
            "icaMail" : None  
        }

        if managerIDICA_Admin != None:   
            icaAdminIDUser = session.query(ICAAdmin).filter_by(idICA_Admin = managerIDICA_Admin.idICA_Admin).first().idUser
            icaAdminMail = session.query(User).filter_by(idUser = icaAdminIDUser).first().mail

            
            resultICA = {
                "idICA_Admin" : icaAdminIDUser,
                "icaMail" : icaAdminMail 
            }
     
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return resultICA, 200

@manager.route("/deleteIcaAdminFromManager", methods=['POST'])
@cross_origin()
@flask_login.login_required
@manager_or_OpManager.require(http_exception=403)
def deleteIcaAdminFromManager():
    try:
        session = Session(connection.e)
        
        icaAdminMailReq = flask.request.json['icaAdminMail']
        
        icaAdminUserQuery = session.query(User).filter_by(mail = icaAdminMailReq).first()
        
        if icaAdminUserQuery == None:
            return "IcaAdmin does not exist"
         
        icaAdminQuery = session.query(ICAAdmin).filter_by(idUser = icaAdminUserQuery.idUser).first()
        
        session.query(Manager).\
            filter_by(idICA_Admin = icaAdminQuery.idICA_Admin).\
            update({
                Manager.idICA_Admin: None
            })

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e) 

    session.close()
    return "Ica Admin unassigned", 200
