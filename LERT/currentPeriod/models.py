from LERT.db.database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class CurrentPeriod(Base):
    __tablename__='CurrentPeriod'

    idCurrentPeriod = Column(Integer, primary_key=True)
    quarter = Column(Integer)
    year = Column(Integer)
    key = Column(Integer)
    status = Column(String(30))

    expense = relationship("Expense")
    

