from flask import Blueprint

manager = Blueprint('manager', __name__)

@manager.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
