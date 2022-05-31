from crypt import methods
from flask import Blueprint
import flask_login
from flask_cors import cross_origin
import flask
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.expense.models import Expense
from LERT.endpoints.expenseType.models import ExpenseType
from LERT.endpoints.currentPeriod.models import CurrentPeriod
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.user.models import User
from LERT.endpoints.hourType.models import HourType
from LERT.endpoints.resourceExpense.models import ResourceExpense
import requests

expense = Blueprint('expense', __name__)

session = Session(connection.e)

@expense.route("/createExpense", methods=['POST'])
@cross_origin()
@flask_login.login_required
def createExpense():
    # TODO ExpenseType type es UNIQUE
    # TODO CurrentPeriod PK = quarter + year 
    # TODO tipo de dato de date -> Date !String
            
    statusCode = flask.Response(status=201)
    costReq = int(flask.request.json['cost'])
    dateReq = flask.request.json['date']
    # y, m, d = startDateReq.split('-')
    # startDateReq = datetime.datetime(int(y), int(m), int(d))
    commentReq = flask.request.json['comment']
    nameExpenseReq = flask.request.json['nameExpense']
    keyCurrentPeriodReq = int(flask.request.json['keyCurrentPeriod'])

    try:
        managerMail = flask_login.current_user.id
        managerUserQuery = session.query(User).filter_by(mail = managerMail)
        managerUserID = managerUserQuery.first().idUser 

        managerQuery = session.query(Manager).filter_by(idUser = managerUserID)
        managerID = managerQuery.first().idManager 
             
        
        expenseTypeQuery = session.query(ExpenseType).filter_by(type = nameExpenseReq)
        expenseTypeID = expenseTypeQuery.first().idExpenseType
        
        currentPeriodQuery = session.query(CurrentPeriod).filter_by(key = keyCurrentPeriodReq)
        currentPeriodID = currentPeriodQuery.first().idCurrentPeriod
            
    except Exception as e:
        print(e)

    try:
        
        expense1 = Expense(idManager = managerID, idExpenseType = expenseTypeID, 
        idCurrentPeriod =  currentPeriodID ,cost = costReq, date = dateReq, comment = commentReq)
        session.add(expense1)
        session.commit() 

        if nameExpenseReq == "Salary" or nameExpenseReq == "Double" or nameExpenseReq == "Triple":
            rateReq = flask.request.json['cost']

            hourTypeQuery = session.query(HourType).filter_by(type = nameExpenseReq)
            hourTypeID = hourTypeQuery.first().idHourType
            
            resourceExpense1 = ResourceExpense(idHourType = hourTypeID, idExpense = expense1.idExpense, rate = rateReq)
            session.add(resourceExpense1)
            session.commit() 
        
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    return statusCode


session.close()
