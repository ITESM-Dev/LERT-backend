from flask import Blueprint

ica = Blueprint('ica', __name__)

@ica.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
