from crypt import methods
import datetime
from sys import stderr
from flask import Blueprint, jsonify
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
from LERT.endpoints.authorization.roles import opManager_permission, icaAdmin_permission
from flask_cors import cross_origin
import requests

manager = Blueprint('manager', __name__)

session = Session(connection.e)

@manager.route("/setOpManager", methods=['POST'])
@cross_origin()
@flask_login.login_required
def setOpManager():
    try:
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

    return "Manager assigned to OpManager", 200

@manager.route("/setIcaAdmin", methods=['POST'])
@cross_origin()
@flask_login.login_required
def setIcaAdmin():
    try:
        managerMail = flask.request.json['managerMail']
        icaAdminMail = flask_login.current_user.id

        managerQuery = session.query(User).filter_by(mail = managerMail)
        icaAdminUserQuery = session.query(User).filter_by(mail = icaAdminMail)
        icaAdminUserID = icaAdminUserQuery.first().idUser
        icaAdminQuery = session.query(ICAAdmin).filter_by(idUser = icaAdminUserID)
        icaAdminID = icaAdminQuery.first().idICA_Admin
        managerID = managerQuery.first().idUser
        
        session.query(Manager).\
            filter_by(idUser = managerID).\
            update({Manager.idICA_Admin: icaAdminID})
        session.commit()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return "Manager assigned to IcaAdmin", 200

@manager.route("/assignResourceToManager", methods=['POST'])
@cross_origin()
@flask_login.login_required
def assignResourceToManager():
    try:
        managerMail = flask_login.current_user.id
        resourceMailReq = flask.request.json['resourceMail']

        resourceUserID = session.query(User).filter_by(mail = resourceMailReq).first().idUser
        resourceID = session.query(Resource).filter_by(idUser = resourceUserID).first().idSerial

        print(resourceID, file=stderr)

        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser
        managerID = session.query(Manager).filter_by(idUser = managerUserID).first().idManager
        print(managerID, file=stderr)

        
        association_manager_resource = association_table_Manager_Resource.insert().values(idSerial = resourceID, idManager = managerID)
        session.execute(association_manager_resource) 
        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return "OK", 200

@manager.route("/getManagerICA", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getManagerICA():
    try:
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

    return resultICA, 200

@manager.route("/getAvailableResources", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getAvailableResources():
    try:
        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser
        managerID = session.query(Manager).filter_by(idUser = managerUserID).first().idManager

        resources = session.query(association_table_Manager_Resource).filter(association_table_Manager_Resource.c.idManager != managerID).all()
        
        resultResources = []

        for current in resources:

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

    return jsonify(resultResources), 200
    
@manager.route("/getResources", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getResources():
    try:
        managerMail = flask_login.current_user.id
        managerUserID = session.query(User).filter_by(mail = managerMail).first().idUser
        managerID = session.query(Manager).filter_by(idUser = managerUserID).first().idManager

        resources = session.query(association_table_Manager_Resource).filter(association_table_Manager_Resource.c.idManager == managerID).all()
        
        resultResources = []

        for current in resources:

            currResource = session.query(Resource).filter_by(idSerial = current.idSerial).first()
            currResourceUserInfo = session.query(User).filter_by(idUser = currResource.idUser).first()

            currentResource = {
                "id": currResource.idUser,
                "name": currResourceUserInfo.name,
                "mail": currResourceUserInfo.mail,
                "role": currResourceUserInfo.role,
                "country":currResourceUserInfo.country
            }

            resultResources.append(currentResource)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return jsonify(resultResources), 200


@manager.route("/updateResources", methods=['POST'])
@cross_origin()
@flask_login.login_required
def updateResources():
    try:
        idResourceReq = flask.request.json['id']
        resourceNameReq = flask.request.json['name']
        resourceBandReq = int(flask.request.json['band'])
        resourceRoleReq = flask.request.json['role']
        resourceCountryReq = flask.request.json['country']

        session.query(User).filter_by(
            idUser = idResourceReq
            ).update(
                {
                    User.name: resourceNameReq, 
                    User.band: resourceBandReq, 
                    User.role: resourceRoleReq,
                    User.country: resourceCountryReq
                }
            )

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)
    return "Resource updated", 200

@manager.route("/getExpenses", methods=['GET'])
@cross_origin()
@flask_login.login_required
def getExpenses():

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
        print(managerIdICA, file =stderr)
        idUserICAAdmin = session.query(ICAAdmin).filter_by(idICA_Admin = managerIdICA).first().idUser
        mailICAAdmin = session.query(User).filter_by(idUser = idUserICAAdmin).first().mail
        idUserOpManager = session.query(OpManager).filter_by(idOPManager = managerIdOPManager).first().idUser
        mailOPManager = session.query(User).filter_by(idUser = idUserOpManager).first().mail
        
        current = {
            'id_expense': expense.idExpense,
            "type": expenseType,
            "cost": expense.cost,
            "date": expense.date,
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
        
    return jsonify(result_expenses), 200

@manager.route("/updateExpense", methods=['POST'])
@cross_origin()
@flask_login.login_required
def updateExpenses():
    try:
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
    return "Expense updated" ,200

@manager.route("/deleteExpense", methods=['POST'])
@cross_origin()
@flask_login.login_required
def deleteExpenses():
    try:
        expenseIDReq = int(flask.request.json['id'])
        expenseDB = session.query(Expense).filter_by(idExpense = expenseIDReq).first()
        session.delete(expenseDB)
        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    except Exception as e:
        print(e) 

    return "Expense Deleted", 200

@manager.route("/expensesForQuarter", methods=['POST'])
@cross_origin()
@flask_login.login_required
def expensesForQuarter():
    
    try: 

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

    return quarters, 200
    

session.close()


