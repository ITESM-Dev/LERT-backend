from flask import Blueprint

expenseType = Blueprint('expenseType', __name__)

@expenseType.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
