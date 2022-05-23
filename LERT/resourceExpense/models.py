from LERT.db.database import db

class ResourceExpense(db.Model):
    idResourceExpense = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Float)