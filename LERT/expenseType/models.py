from LERT.db.database import db


class ExpenseType(db.Model):
    idExpenseType = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200))

#def __init__(self, name, email):
#    self.name = name
#    self.email = email
