from LERT.db.database import db

association_table_Expense_Resource = db.Table(
    'association', db.metadata,
    db.Column('idExpense', db.Integer, db.ForeignKey('Expense.idExpense')),
    db.Column('idResource', db.Integer, db.ForeignKey('Resource.idSerial'))
)

association_table_Expense_ICA = db.Table(
    'association', db.metadata,
    db.Column('idExpense', db.Integer, db.ForeignKey('Expense.idExpense')),
    db.Column('idICA', db.Integer, db.ForeignKey('ICA.idICA'))
)
class Expense(db.Model):
    __tablename__ = 'Expense'

    idExpense = db.Column(db.Integer, primary_key=True)
    idManager = db.Column(db.Integer, db.ForeignKey('Manager.idManager'))
    idExpenseType = db.Column(db.Integer, db.ForeignKey('ExpenseType.idExpenseType'))
    cost = db.Column(db.Float)
    date = db.Column(db.String(100))
    comment = db.Column(db.String(255))
    resource = db.relationship("Resource", secondary=association_table_Expense_Resource)
    ica = db.relationship("ICA", secondary=association_table_Expense_ICA)
    expenseType = db.relationship("ExpenseType", back_populates="expense")
    resourceExpense = db.relationship("ResourceExpense", back_populates="expense", uselist=False)