from LERT.db.database import Base
from LERT.hourType.models import HourType
from LERT.expense.models import Expense
from sqlalchemy import *
from sqlalchemy.orm import relationship

class ResourceExpense(Base):
    print("Test resource")
    __tablename__ = 'ResourceExpense'
    
    idResourceExpense = Column(Integer, primary_key=True)
    idHourType = Column(Integer, ForeignKey(HourType.idHourType))
    idExpense = Column(Integer, ForeignKey(Expense.idExpense))
    rate = Column(Float)
    expense = relationship("Expense", back_populates="resourceExpense")
    hourType = relationship("HourType", back_populates="resourceExpense")