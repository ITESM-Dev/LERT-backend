from LERT.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

class ExpenseType(Base):
    __tablename__ = "ExpenseType"

    idExpenseType = Column(Integer, primary_key=True)
    type = Column(String(200))

    expense = relationship("Expense", back_populates="expenseType", uselist=False)

