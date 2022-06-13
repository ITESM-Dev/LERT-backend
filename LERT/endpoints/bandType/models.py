from LERT.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

class BandType(Base):
    __tablename__ = 'BandType'

    idBandType = Column(Integer, primary_key=True)
    type = Column(String(200))
    band = Column(String(50))
    country = Column(String(120))
    yearlyRate = Column(Float) 
    dateToStart = Column(Date)
    dateToFinish = Column(Date)

    hourType = relationship('HourType', back_populates="bandType", uselist=False)