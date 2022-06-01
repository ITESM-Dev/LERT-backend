from flask import Blueprint

currentPeriod = Blueprint('currentPeriod', __name__)

@currentPeriod.route("/")
def hello():
    return "hello"