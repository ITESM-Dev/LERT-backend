from flask import Blueprint
from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.administrator.models import Administrator

admin = Blueprint('admin', __name__)

try:
    session = Session(connection.e)

    #admin1 = Administrator(idUser=1)
    #session.add(admin1)
    #session.commit() 
    session.close()
except Exception as e:
    print(e)

@admin.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
