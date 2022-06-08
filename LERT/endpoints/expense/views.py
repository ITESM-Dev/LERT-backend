from crypt import methods
from sys import stderr
from flask import Blueprint
import flask_login
from flask_cors import cross_origin
import flask
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.expense.models import Expense
from LERT.endpoints.expense.models import association_table_Expense_Resource
from LERT.endpoints.resource.models import Resource
from LERT.endpoints.expenseType.models import ExpenseType
from LERT.endpoints.ica.models import ICA
from LERT.endpoints.currentPeriod.models import CurrentPeriod
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.user.models import User
from LERT.endpoints.hourType.models import HourType
from LERT.endpoints.resourceExpense.models import ResourceExpense
import datetime
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
            
    try:
        mailReq = flask.request.json['mailResource']
        costReq = int(flask.request.json['cost'])
        dateReq = flask.request.json['date']
        commentReq = flask.request.json['comment']
        nameExpenseReq = flask.request.json['nameExpense']
        keyCurrentPeriodReq = int(flask.request.json['keyCurrentPeriod'])

        y, m, d = dateReq.split('-')
        dateFormat = datetime.datetime(int(y), int(m), int(d))

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
        idCurrentPeriod =  currentPeriodID ,cost = costReq, date = dateFormat, comment = commentReq)
        session.add(expense1)
        session.commit() 

        if nameExpenseReq == "Salary" or nameExpenseReq == "Double" or nameExpenseReq == "Triple":
            rateReq = flask.request.json['cost']

            hourTypeQuery = session.query(HourType).filter_by(type = nameExpenseReq)
            hourTypeID = hourTypeQuery.first().idHourType
            
            resourceExpense1 = ResourceExpense(idHourType = hourTypeID, idExpense = expense1.idExpense, rate = rateReq)
            session.add(resourceExpense1)
            session.commit() 

        resourceUser = session.query(User).filter_by(mail = mailReq).first()
        resourceUserID = resourceUser.idUser
        resourceQuery = session.query(Resource).filter_by(idUser = resourceUserID).first()
        resourceID = resourceQuery.idSerial

        association_expense_resource = association_table_Expense_Resource.insert().values(idExpense = expense1.idExpense, idResource = resourceID)
        session.execute(association_expense_resource) 
        session.commit()        
        
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    id = {"id": expense1.idExpense }
    
    return id, 201 


session.close()
