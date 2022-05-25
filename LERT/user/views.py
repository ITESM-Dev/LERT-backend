from flask import Blueprint
#from LERT.db.session import session
from LERT.db.database import connection
from sqlalchemy.orm import Session
from LERT.user.models import User

user = Blueprint('user', __name__)

try:
    session = Session(connection.e)

#    user1 = User(name = "test name 2", mail = "fffd@test.com", password = "testpassword",
#    token = "testToken", expiration = 8, role = "Admin")
#    session.add(user1)
#    session.commit() 
    session.close()
except Exception as e:
    print(e)

@user.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
