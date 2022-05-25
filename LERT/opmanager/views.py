from flask import Blueprint

opManager = Blueprint('opManager', __name__)

@opManager.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
