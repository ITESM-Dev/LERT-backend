from LERT.db.database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

association_table_Expense_Resource = Table(
    'association', Base.metadata,
    Column('idExpense', Integer, ForeignKey('Expense.idExpense')),
    Column('idResource', Integer, ForeignKey('Resource.idSerial'))
)

association_table_Expense_ICA = Table(
    'association', Base.metadata,
    Column('idExpense', Integer, ForeignKey('Expense.idExpense')),
    Column('idICA', Integer, ForeignKey('ICA.idICA'))
)
class Expense(Base):
    __tablename__ = 'Expense'

    idExpense = Column(Integer, primary_key=True)
    idManager = Column(Integer, ForeignKey('Manager.idManager'))
    idExpenseType = Column(Integer, ForeignKey('ExpenseType.idExpenseType'))
    cost = Column(Float)
    date = Column(String(100))
    comment = Column(String(255))
    resource = relationship("Resource", secondary=association_table_Expense_Resource)
    ica = relationship("ICA", secondary=association_table_Expense_ICA)
    expenseType = relationship("ExpenseType", back_populates="expense")
    resourceExpense = relationship("ResourceExpense", back_populates="expense", uselist=False)