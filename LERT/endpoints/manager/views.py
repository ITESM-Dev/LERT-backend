from flask import Blueprint
import flask
import flask_login
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.user.models import User

manager = Blueprint('manager', __name__)

session = Session(connection.e)

@manager.route("/setOpManager")
def setOpManager():
    managerMail = flask.request.form['ManagerMail']
    opManagerID = flask_login.current_user.id

    userDBQuery = session.query(User).filter_by(mail = managerMail)
    userDBID = userDBQuery.first().id

    session.query(Manager).\
        filter_by(idManager = userDBID).\
        update({Manager.idOPManager: opManagerID})

session.close()