from flask import Blueprint

bandType = Blueprint('bandType', __name__)

@bandType.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
