from LERT.db.database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

association_table_Expense_Resource = Table(
    'expense_resource', Base.metadata,
    Column('idExpense', Integer, ForeignKey('Expense.idExpense')),
    Column('idResource', Integer, ForeignKey('Resource.idSerial'))
)

class Expense(Base):
    __tablename__ = 'Expense'

    idExpense = Column(Integer, primary_key=True)
    idManager = Column(Integer, ForeignKey('Manager.idManager'))
    idExpenseType = Column(Integer, ForeignKey('ExpenseType.idExpenseType'))
    cost = Column(Float)
    date = Column(Date)
    comment = Column(String(255))
    idCurrentPeriod = Column(Integer, ForeignKey("CurrentPeriod.idCurrentPeriod"))
    resource = relationship("Resource", secondary=association_table_Expense_Resource)
    expenseType = relationship("ExpenseType", back_populates="expense")
    resourceExpense = relationship("ResourceExpense", back_populates="expense", uselist=False)
    