from LERT.db.database import db


class ExpenseType(db.Model):
    __tablename__ = "ExpenseType"

    idExpenseType = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200))

    expense = db.relationship("Expense", back_populates="expenseType", uselist=False)

