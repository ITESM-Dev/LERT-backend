from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
