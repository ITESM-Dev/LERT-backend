from LERT.db.database import db

association_table = db.Table(
    'association', db.metadata,
    db.Column('idExpense', db.Integer, db.ForeignKey('Expense.idExpense')),
    db.Column('idResource', db.Integer, db.ForeignKey('Resource.idSerial'))
)
class Expense(db.Model):
    __tablename__ = 'Expense'

    idExpense = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float)
    date = db.Column(db.String(100))
    comment = db.Column(db.String(255))
    resource = db.relationship("Rexource", secondary=association_table)