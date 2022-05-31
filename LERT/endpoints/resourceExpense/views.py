from flask import Blueprint

resourceExpense = Blueprint('resourceExpense', __name__)

@resourceExpense.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
