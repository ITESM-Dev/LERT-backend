from LERT.db.database import db


class Expense(db.Model):
    idExpense = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float)
    date = db.Column(db.String(100))
    comment = db.Column(db.String(255))