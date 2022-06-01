import json
import os
from flask import jsonify, Flask
from sqlalchemy import *
from LERT.db import database, session
from LERT.ica.views import ica
from LERT.opmanager.views import opManager
from LERT.manager.views import manager
from LERT.expenseType.views import expenseType
from LERT.hourType.views import hourType
from LERT.bandType.views import bandType
from LERT.user.views import user
from LERT.administrator.views import admin
from LERT.icaAdmin.views import icaAdmin
from LERT.resource.views import resource
from LERT.expense.views import expense
from LERT.resourceExpense.views import resourceExpense

from db2_Connection import Db2Connection

app = Flask(__name__, static_url_path='')

def create_app():

    if os.getenv('ENVIRONMENT') == 'dev':
        app.config.from_object('config.DevelopmentConfig')
        print(os.getenv('ENVIRONMENT'))
    elif os.getenv('ENVIRONMENT') == 'prod':
        app.config.from_object('config.DevelopmentConfig')
        print(os.getenv('ENVIRONMENT'))
    database
    session

app.register_blueprint(user)
app.register_blueprint(admin)
app.register_blueprint(icaAdmin)
app.register_blueprint(resource)
app.register_blueprint(expense)
app.register_blueprint(resourceExpense)
app.register_blueprint(ica)
app.register_blueprint(opManager)
app.register_blueprint(manager)
app.register_blueprint(expenseType)
app.register_blueprint(hourType)
app.register_blueprint(bandType)

#sentence = "SELECT * FROM OOLONG"
#rows = connection.get_all(sentence)
#print(rows)
#connection._create_connection_sqlAlchemy()

# @app.route("/")
# def hello():
#     return "<h1 style='color:blue'>Hello There!</h1>"

# @app.route("/user")
# def get_user():
#     Dictionary ={'id':'eduCBA' , 'user_name':'Premium' , 'user_last_name':'2709 days'}
#     return jsonify(Dictionary)

if __name__ == "__main__":
    create_app().run()