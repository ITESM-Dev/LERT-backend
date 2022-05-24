from flask import Blueprint

resource = Blueprint('resource', __name__)

@resource.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
