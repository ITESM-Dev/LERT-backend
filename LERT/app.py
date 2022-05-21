from flask import Flask
from sqlalchemy import *
from LERT.db import database
from LERT.user.views import user

app = Flask(__name__)

def create_app():
    app.config.from_object('config.DevelopmentConfig')
    #database.init_app()
    
app.register_blueprint(user)

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