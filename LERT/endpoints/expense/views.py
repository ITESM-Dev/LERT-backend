from flask import Blueprint

expense = Blueprint('expense', __name__)

@expense.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
