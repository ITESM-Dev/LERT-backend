from flask import Blueprint
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.icaAdmin.models import ICAAdmin

icaAdmin = Blueprint('icaAdmin', __name__)

try:
    session = Session(connection.e)

    #icaAdmin1 = ICAAdmin(idUser=1)
    #session.add(icaAdmin1)
    #session.commit() 
    session.close()
except Exception as e:
    print(e)

@icaAdmin.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
