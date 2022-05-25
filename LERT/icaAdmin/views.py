from flask import Blueprint

icaAdmin = Blueprint('icaAdmin', __name__)

@icaAdmin.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
