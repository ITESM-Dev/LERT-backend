from flask import Blueprint
import flask_login
from flask_cors import cross_origin
import flask
from sqlalchemy.orm import Session
from LERT.db.database import connection
import requests
from LERT.endpoints.expenseType.models import ExpenseType

expenseType = Blueprint('expenseType', __name__)

session = Session(connection.e)

@expenseType.route("/createExpenseType", methods=['POST'])
@cross_origin()
@flask_login.login_required
def createExpenseType():

    statusCode = flask.Response(status=201)
    typeReq = flask.request.json['type']

    try:
        
        expenseType1 = ExpenseType(type = typeReq)
        session.add(expenseType1)
        session.commit() 
        
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)
        
    return statusCode


session.close()
