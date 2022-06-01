from flask import Blueprint
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.opmanager.models import OpManager

opManager = Blueprint('opManager', __name__)

try:
    session = Session(connection.e)

    #opManager2 = OpManager(idUser=1, country="Mexico", status="Active")
    #session.add(opManager2)
    #session.commit() 
    session.close()
except Exception as e:
    print(e)

@opManager.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
