from LERT.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

class HourType(Base):
    __tablename__ = "HourType"

    idHourType = Column(Integer, primary_key=True)
    idBandType = Column(Integer, ForeignKey('BandType.idBandType'))
    type = Column(String(200))
    band = Column(String(50))
    country = Column(String(120))
    rate = Column(Float)
    dateToStart = Column(Date)
    dateToFinish = Column(Date)

    resourceExpense = relationship("ResourceExpense", back_populates="hourType", uselist=False)
    bandType = relationship("BandType", back_populates="hourType")