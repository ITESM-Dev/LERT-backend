from sys import stderr
from flask import Blueprint
import flask
from flask_cors import cross_origin
import flask_login
import requests
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.administrator.models import Administrator
from LERT.endpoints.user.models import User
from LERT.endpoints.authorization.roles import admin_permission

admin = Blueprint('admin', __name__)

@admin.route("/updateUserRoles", methods=['POST'])
@cross_origin()
@flask_login.login_required
@admin_permission.require(http_exception=403)
def getUserInfo():
    session = Session(connection.e)
    try:
        userMailReq = flask.request.json['mail']
        roleReq = flask.request.json['role']

        userDBQuery = session.query(User).filter_by(mail = userMailReq)

        userDBQuery.\
        update({User.role: roleReq}, synchronize_session='fetch')

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return "User role updated", 200

@admin.route("/deleteUserRoles", methods=['POST'])
@cross_origin()
@flask_login.login_required
@admin_permission.require(http_exception=403)
def deleteUserRoles():
    session = Session(connection.e)
    try:
        userMailReq = flask.request.json['mail']

        userDBQuery = session.query(User).filter_by(mail = userMailReq)
        
        userDBQuery.\
        update({User.role: "Resource"}, synchronize_session='fetch')

        session.commit()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)        
    except Exception as e:
        print(e)

    session.close()
    return "User role Deleted", 200