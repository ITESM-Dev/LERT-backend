from flask import Blueprint

OpManager = Blueprint('OpManager', __name__)

@OpManager.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
