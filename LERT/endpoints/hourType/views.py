from flask import Blueprint

hourType = Blueprint('hourType', __name__)

@hourType.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
