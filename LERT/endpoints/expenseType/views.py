from flask import Blueprint, jsonify
import flask_login
from flask_cors import cross_origin
import flask
from sqlalchemy.orm import Session
from LERT.db.database import connection
import requests
from LERT.endpoints.expenseType.models import ExpenseType
from LERT.endpoints.authorization.roles import manager_or_OpManager_or_icaAdmin, opManager_permission

expenseType = Blueprint('expenseType', __name__)

@expenseType.route("/createExpenseType", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def createExpenseType():

    typeReq = flask.request.json['type']

    try:

        session = Session(connection.e)
        
        expenseType1 = ExpenseType(type = typeReq)
        session.add(expenseType1)
        session.commit() 

        session.close()
        
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)
        
    id = {"id": expenseType1.idExpenseType }

    return id, 201 

@expenseType.route("/getExpenseTypes", methods=['GET'])
@cross_origin()
@flask_login.login_required
@manager_or_OpManager_or_icaAdmin.require(http_exception=403)
def getExpenseType():
    try:
        session = Session(connection.e)

        expenseTypes = session.query(ExpenseType).all()

        resultTypes = []

        for current in expenseTypes:
            
            currentManager = {
                "idExpenseType": current.idExpenseType,
                "type": current.type
            }

            resultTypes.append(currentManager)

        session.close()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)
    return jsonify(resultTypes), 200

@expenseType.route("/updateExpenseType", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def updateExpenseType():
    try:
        session = Session(connection.e)

        idExpenseTypeReq = flask.request.json['id']
        expenseTypeReq = flask.request.json['type']

        expenseTypeQuery = session.query(ExpenseType).filter_by(idExpenseType = idExpenseTypeReq)
        
        expenseTypeQuery.\
        update({ExpenseType.type: expenseTypeReq}, synchronize_session='fetch')

        session.commit()

        session.close()
        
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return "Expense Type updated" ,200

@expenseType.route("/deleteExpenseType", methods=['POST'])
@cross_origin()
@flask_login.login_required
@opManager_permission.require(http_exception=403)
def deleteExpenseType():
    try:
        session = Session(connection.e)

        idExpenseTypeReq = flask.request.json['id']

        expenseTypeQuery = session.query(ExpenseType).filter_by(idExpenseType = idExpenseTypeReq).first()
        session.delete(expenseTypeQuery)
        session.commit()

        session.close()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return "Expense Type Deleted" ,200
