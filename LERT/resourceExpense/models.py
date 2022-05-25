from LERT.db.database import db

class ResourceExpense(db.Model):
    __tablename__ = 'ResourceExpense'
    
    idResourceExpense = db.Column(db.Integer, primary_key=True)
    idHourType = db.Column(db.Integer, db.ForeignKey("HourType.idHourType"))
    idExpense = db.Column(db.Integer, db.ForeignKey("Expense.idExpense"))
    rate = db.Column(db.Float)
    expense = db.relationship("Expense", back_populates="resourceExpense")
    hourType = db.relationship("HourType", back_populates="resourceExpense")